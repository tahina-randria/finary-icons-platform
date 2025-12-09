"""
YouTube Transcript Extraction Service
"""

from youtube_transcript_api import YouTubeTranscriptApi
from app.core.logging import logger
from typing import Optional, Dict, Any
import re
from urllib.parse import urlparse, parse_qs


class YouTubeService:
    """Service for extracting transcripts from YouTube videos"""

    def __init__(self):
        """Initialize YouTube service"""
        logger.info("YouTube service initialized")

    def extract_video_id(self, youtube_url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats

        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        """
        try:
            parsed_url = urlparse(str(youtube_url))

            # youtube.com/watch?v=VIDEO_ID
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    return query_params.get('v', [None])[0]
                # youtube.com/embed/VIDEO_ID
                elif parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/')[2]

            # youtu.be/VIDEO_ID
            elif parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]

            # Try regex as fallback
            match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', str(youtube_url))
            if match:
                return match.group(1)

            return None

        except Exception as e:
            logger.error(f"Failed to extract video ID: {str(e)}")
            return None

    async def get_transcript(
        self,
        youtube_url: str,
        languages: list[str] = ['fr', 'en']
    ) -> Dict[str, Any]:
        """
        Get transcript from YouTube video

        Args:
            youtube_url: YouTube video URL
            languages: Preferred languages (in order)

        Returns:
            Dict with video_id, transcript, and metadata
        """
        try:
            # Extract video ID
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                raise ValueError(f"Could not extract video ID from URL: {youtube_url}")

            logger.info(f"Fetching transcript for video: {video_id}")

            # Get transcript
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to get transcript in preferred languages
            transcript = None
            language_used = None

            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    language_used = lang
                    break
                except:
                    continue

            # Fallback to any available transcript
            if not transcript:
                transcript = transcript_list.find_generated_transcript(['en', 'fr'])
                language_used = transcript.language_code

            # Fetch transcript data
            transcript_data = transcript.fetch()

            # Combine all text segments
            full_text = " ".join([entry['text'] for entry in transcript_data])

            # Calculate duration
            if transcript_data:
                duration = transcript_data[-1]['start'] + transcript_data[-1]['duration']
            else:
                duration = 0

            logger.info(f"Successfully fetched transcript ({len(full_text)} chars)")

            return {
                "video_id": video_id,
                "transcript": full_text,
                "segments": transcript_data,
                "language": language_used,
                "duration_seconds": duration,
                "word_count": len(full_text.split())
            }

        except Exception as e:
            logger.error(f"Failed to get transcript for {youtube_url}: {str(e)}")
            raise

    async def get_transcript_segments(
        self,
        youtube_url: str,
        min_duration: float = 5.0
    ) -> list[Dict[str, Any]]:
        """
        Get transcript as time-segmented chunks

        Useful for extracting concepts from specific parts of the video
        """
        try:
            result = await self.get_transcript(youtube_url)
            segments = result['segments']

            # Group segments by minimum duration
            grouped_segments = []
            current_group = []
            current_duration = 0

            for segment in segments:
                current_group.append(segment)
                current_duration += segment['duration']

                if current_duration >= min_duration:
                    grouped_segments.append({
                        "text": " ".join([s['text'] for s in current_group]),
                        "start": current_group[0]['start'],
                        "duration": current_duration
                    })
                    current_group = []
                    current_duration = 0

            # Add remaining segments
            if current_group:
                grouped_segments.append({
                    "text": " ".join([s['text'] for s in current_group]),
                    "start": current_group[0]['start'],
                    "duration": current_duration
                })

            return grouped_segments

        except Exception as e:
            logger.error(f"Failed to segment transcript: {str(e)}")
            raise


# Singleton instance
youtube_service = YouTubeService()
