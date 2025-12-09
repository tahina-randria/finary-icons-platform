"""
Concept Extraction Service using GPT-4
Extracts ALL concepts (not just financial) from transcripts
"""

from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import logger
from app.models.generation import ConceptExtraction, ConceptPriority
from typing import List, Dict, Any
import json


# 12 Categories for concept extraction
CATEGORIES = {
    "finance_investissement": {
        "description": "Financial instruments, investment types, trading",
        "examples": ["Actions", "Obligations", "Crypto", "ETF", "PEA"],
        "visual_style": "Professional financial icon with depth"
    },
    "immobilier": {
        "description": "Real estate, property, housing",
        "examples": ["Maison", "Appartement", "SCPI", "Garage", "Terrain"],
        "visual_style": "Architectural icon with structure"
    },
    "vehicules": {
        "description": "Cars, transportation, vehicles",
        "examples": ["Voiture", "Moto", "Bateau", "Avion", "Vélo"],
        "visual_style": "Sleek vehicle icon with motion feel"
    },
    "metiers": {
        "description": "Professions, jobs, occupations",
        "examples": ["Médecin", "Ingénieur", "Professeur", "Chef", "Plombier"],
        "visual_style": "Professional icon representing the occupation"
    },
    "objets": {
        "description": "Objects, items, possessions",
        "examples": ["Montre", "Téléphone", "Livre", "Clé", "Outil"],
        "visual_style": "Clean product icon with detail"
    },
    "lieux": {
        "description": "Places, locations, venues",
        "examples": ["Paris", "Bureau", "Restaurant", "Hôpital", "Aéroport"],
        "visual_style": "Location icon with identifying features"
    },
    "devises": {
        "description": "Currencies, money",
        "examples": ["Euro", "Dollar", "Bitcoin", "Couronne norvégienne", "Yen"],
        "visual_style": "Currency symbol with elegant design"
    },
    "actions": {
        "description": "Actions, activities, verbs",
        "examples": ["Acheter", "Vendre", "Investir", "Épargner", "Transférer"],
        "visual_style": "Action icon with dynamic feel"
    },
    "etats": {
        "description": "Countries, states, nations",
        "examples": ["France", "USA", "Norvège", "Japon", "Allemagne"],
        "visual_style": "Flag or landmark representation"
    },
    "organismes": {
        "description": "Organizations, institutions, companies",
        "examples": ["Banque", "Assurance", "Entreprise", "ONG", "Gouvernement"],
        "visual_style": "Institutional icon with authority"
    },
    "nourriture": {
        "description": "Food, drinks, cuisine",
        "examples": ["Pain", "Vin", "Café", "Restaurant", "Fruits"],
        "visual_style": "Appetizing food icon"
    },
    "sport": {
        "description": "Sports, athletics, fitness",
        "examples": ["Football", "Tennis", "Gym", "Course", "Natation"],
        "visual_style": "Dynamic sports icon with energy"
    }
}


class ConceptExtractionService:
    """Service for extracting concepts from text using GPT-4"""

    def __init__(self):
        """Initialize OpenAI client"""
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("OpenAI client configured for concept extraction")
        else:
            self.client = None
            logger.warning("OpenAI API key not configured")

    def _build_extraction_prompt(self, transcript: str, max_concepts: int = 30) -> str:
        """Build prompt for GPT-4 to extract concepts"""

        categories_desc = "\n".join([
            f"- {cat}: {info['description']} (Examples: {', '.join(info['examples'])})"
            for cat, info in CATEGORIES.items()
        ])

        prompt = f"""You are an expert at extracting visual concepts from text for icon generation.

Extract ALL important concepts from this transcript that could be represented as icons.
NOT JUST financial concepts - extract EVERYTHING: objects, places, currencies, professions, vehicles, food, sports, etc.

Categories:
{categories_desc}

Transcript:
{transcript}

Extract up to {max_concepts} concepts and for each provide:
1. name: The concept name (concise, 1-3 words)
2. category: One of the categories listed above
3. priority: high (very important), medium (relevant), low (minor)
4. visual_description: Detailed description for AI image generation (2-3 sentences)
5. context: Brief context from transcript where it appears

Return as JSON array:
[
  {{
    "name": "Bitcoin",
    "category": "devises",
    "priority": "high",
    "visual_description": "A golden coin with the Bitcoin 'B' symbol, metallic finish with depth and shine, representing digital cryptocurrency.",
    "context": "investing in Bitcoin for long-term growth"
  }},
  ...
]

Focus on concepts that:
- Are visually representable as icons
- Are mentioned explicitly or implied strongly
- Would be useful for motion design and video analysis
- Cover diverse categories (not just finance)

Return ONLY the JSON array, no other text."""

        return prompt

    async def extract_concepts(
        self,
        transcript: str,
        max_concepts: int = 30,
        min_priority: ConceptPriority = ConceptPriority.MEDIUM
    ) -> List[ConceptExtraction]:
        """
        Extract concepts from transcript using GPT-4

        Args:
            transcript: Text transcript to analyze
            max_concepts: Maximum number of concepts to extract
            min_priority: Minimum priority level to include

        Returns:
            List of extracted concepts
        """
        if not self.client:
            raise Exception("OpenAI client not initialized")

        try:
            logger.info(f"Extracting concepts from transcript ({len(transcript)} chars)")

            prompt = self._build_extraction_prompt(transcript, max_concepts)

            # Call GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing content and extracting visual concepts for icon generation. You always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )

            # Parse response
            content = response.choices[0].message.content
            concepts_data = json.loads(content)

            # Convert to ConceptExtraction objects
            concepts = []
            for item in concepts_data:
                # Skip if below minimum priority
                priority = ConceptPriority(item['priority'])
                if min_priority == ConceptPriority.HIGH and priority != ConceptPriority.HIGH:
                    continue
                if min_priority == ConceptPriority.MEDIUM and priority == ConceptPriority.LOW:
                    continue

                concept = ConceptExtraction(
                    name=item['name'],
                    category=item['category'],
                    priority=priority,
                    visual_description=item['visual_description'],
                    context=item.get('context')
                )
                concepts.append(concept)

            logger.info(f"Extracted {len(concepts)} concepts")
            return concepts

        except Exception as e:
            logger.error(f"Failed to extract concepts: {str(e)}")
            raise

    async def check_existing_icon(self, concept_name: str) -> bool:
        """
        Check if icon for this concept already exists
        TODO: Implement database query
        """
        # TODO: Query Supabase to check if icon exists
        return False

    async def filter_new_concepts(
        self,
        concepts: List[ConceptExtraction]
    ) -> List[ConceptExtraction]:
        """Filter out concepts that already have icons"""
        new_concepts = []

        for concept in concepts:
            exists = await self.check_existing_icon(concept.name)
            if not exists:
                new_concepts.append(concept)
            else:
                logger.info(f"Icon already exists for: {concept.name}")

        return new_concepts


# Singleton instance
concept_extraction_service = ConceptExtractionService()
