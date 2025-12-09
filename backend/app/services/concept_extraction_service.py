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

    def _repair_json(self, content: str) -> str:
        """
        Attempt to repair malformed JSON from GPT-4o
        Fixes French apostrophes and other common issues
        """
        import re
        import os
        import tempfile
        from datetime import datetime

        # Save original for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_file = os.path.join(tempfile.gettempdir(), f"gpt4o_response_{timestamp}.json")
        try:
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Saved GPT-4o response to: {debug_file}")
        except Exception as e:
            logger.warning(f"Could not save debug file: {e}")

        # Replace French apostrophe patterns that break JSON
        # d'épargne -> de epargne, l'investissement -> le investissement
        french_patterns = [
            (r"d'(\w)", r"de \1"),
            (r"D'(\w)", r"De \1"),
            (r"l'(\w)", r"le \1"),
            (r"L'(\w)", r"Le \1"),
            (r"s'(\w)", r"se \1"),
            (r"S'(\w)", r"Se \1"),
            (r"n'(\w)", r"ne \1"),
            (r"N'(\w)", r"Ne \1"),
            (r"c'(\w)", r"ce \1"),
            (r"C'(\w)", r"Ce \1"),
            (r"m'(\w)", r"me \1"),
            (r"M'(\w)", r"Me \1"),
            (r"t'(\w)", r"te \1"),
            (r"T'(\w)", r"Te \1"),
            (r"qu'(\w)", r"que \1"),
            (r"Qu'(\w)", r"Que \1"),
        ]

        original = content
        for pattern, replacement in french_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        if content != original:
            logger.info("Applied French apostrophe repairs to JSON")
            # Save repaired version
            repaired_file = os.path.join(tempfile.gettempdir(), f"gpt4o_repaired_{timestamp}.json")
            try:
                with open(repaired_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.debug(f"Saved repaired JSON to: {repaired_file}")
            except Exception as e:
                logger.warning(f"Could not save repaired file: {e}")

        return content

    def _build_extraction_prompt(self, transcript: str, max_concepts: int = 30) -> str:
        """Build prompt for GPT-4 to extract concepts"""

        categories_desc = "\n".join([
            f"- {cat}: {info['description']} (Examples: {', '.join(info['examples'])})"
            for cat, info in CATEGORIES.items()
        ])

        prompt = f"""You are an elite AI specialized in extracting visual concepts from video transcripts for professional 3D icon generation.

YOUR MISSION: Analyze this transcript and extract up to {max_concepts} DIVERSE visual concepts that can be represented as stunning 3D glass-morphism icons.

CATEGORY BALANCE REQUIREMENTS:
- Extract ALL valuable concepts from the transcript, no artificial limits
- Finance concepts are welcome - extract as many quality financial concepts as relevant
- Prioritize diversity across all 12 categories, but dont sacrifice quality for balance
- If the content is heavily financial, extract all important financial concepts
- Aim for variety when possible, but focus on extracting EVERY visually representable concept

ALL 12 CATEGORIES (extract from multiple):
{categories_desc}

EXTRACTION RULES:
1. Prioritize CONCRETE VISUAL elements: objects, places, professions, actions
2. Each concept must be DISTINCT and visually unique
3. Favor specific nouns over generic terms
4. Include abstract concepts ONLY if central and repeatedly mentioned
5. Avoid duplicates or very similar concepts

TRANSCRIPT TO ANALYZE:
{transcript}

VISUAL DESCRIPTION REQUIREMENTS:
- Keep descriptions SHORT and SIMPLE - maximum 2 sentences
- Use ONLY simple words without special punctuation
- NO quotes, NO apostrophes, NO colons, NO semicolons in descriptions
- CRITICAL: Replace French apostrophes with spaces (write "de epargne" not "d'epargne", "le investissement" not "l'investissement")
- Mention materials: glass, metal, wood, leather
- Mention colors: blue, peach, gold, silver
- Mention style: 3D glass icon
- Mention background: black background no reflection

OUTPUT FORMAT - Return ONLY this JSON structure with NO additional text:
{{
  "concepts": [
    {{
      "name": "BookStore",
      "category": "lieux",
      "priority": "high",
      "visual_description": "A small bookstore with wooden shelves and colorful books. 3D glass icon on black background with no reflection.",
      "context": "wants to open a bookstore"
    }}
  ]
}}

CRITICAL: Keep visual_description simple with NO special characters.

VALIDATION CHECKLIST:
- Extract UP TO {max_concepts} concepts (or as many quality concepts as exist in transcript)
- Prioritize quality and relevance over artificial category limits
- Each visual_description is 3-4 sentences with ultra-specific details
- Every description explicitly mentions "3D glass icon" or "3D glass-morphism style"
- Materials, colors, lighting, and form specified for each
- Context quotes or paraphrases the relevant transcript segment
- NO duplicate or overly similar concepts
- Extract ALL important financial concepts if content is finance-focused

PRIORITY GUIDE:
- high: Central topic, mentioned 3+ times, or critically important
- medium: Supporting concept, mentioned 1-2 times clearly
- low: Background element, implied but not explicitly mentioned

Return ONLY valid JSON. NO markdown, NO explanation, NO additional text before or after the JSON.
"""
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
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing content and extracting visual concepts for icon generation. You MUST return ONLY valid JSON with properly escaped quotes in strings. Never use unescaped quotes inside JSON string values."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )

            # Parse response
            content = response.choices[0].message.content
            logger.debug(f"Response content: {content[:500]}")

            # Try to parse JSON, with fallback for malformed JSON
            try:
                concepts_data = json.loads(content)
                logger.info("Successfully parsed JSON on first attempt")
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON on first attempt: {str(e)}")
                logger.warning(f"Error at position {e.pos}, line {e.lineno}, column {e.colno}")
                logger.debug(f"Problematic content around error: {content[max(0, e.pos-100):min(len(content), e.pos+100)]}")

                # STEP 1: Remove markdown code blocks if present
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                    content = content.strip()
                    logger.info("Removed markdown code blocks")

                # STEP 2: Apply French apostrophe repairs
                content = self._repair_json(content)

                # STEP 3: Try parsing again after repairs
                try:
                    concepts_data = json.loads(content)
                    logger.info("✅ Successfully parsed JSON after French apostrophe repairs!")
                except json.JSONDecodeError as e2:
                    logger.warning(f"Failed to parse JSON even after repairs: {str(e2)}")
                    logger.warning(f"Error at position {e2.pos}, line {e2.lineno}, column {e2.colno}")

                    # STEP 4: Last resort - try ast.literal_eval
                    import re
                    try:
                        import ast
                        concepts_data = ast.literal_eval(content)
                        logger.info("Successfully parsed JSON using ast.literal_eval")
                    except:
                        # STEP 5: Final fallback - extract concepts array manually
                        try:
                            match = re.search(r'"concepts"\s*:\s*\[(.*)\]', content, re.DOTALL)
                            if match:
                                logger.warning("Attempting to extract concepts array manually")
                                concepts_data = json.loads('{"concepts": [' + match.group(1) + ']}')
                                logger.info("Successfully extracted concepts array manually")
                            else:
                                logger.error(f"Failed to parse JSON even after all repair attempts")
                                logger.error(f"Content around position {e2.pos}: {content[max(0, e2.pos-200):min(len(content), e2.pos+200)]}")
                                raise Exception(f"Invalid JSON from GPT-4o even after repairs: {str(e2)}")
                        except Exception as e3:
                            logger.error(f"All parsing attempts failed: {str(e3)}")
                            raise Exception(f"Invalid JSON from GPT-4o: {str(e)}")

            # Handle wrapped JSON response from GPT-4o
            if isinstance(concepts_data, dict):
                # Check if concepts are wrapped in a key
                if "concepts" in concepts_data:
                    concepts_data = concepts_data["concepts"]
                elif "items" in concepts_data:
                    concepts_data = concepts_data["items"]
                else:
                    # Check if this is a single concept object (has the expected keys)
                    expected_keys = {'name', 'category', 'priority', 'visual_description'}
                    if expected_keys.issubset(set(concepts_data.keys())):
                        # This is a single concept object, wrap it in an array
                        logger.warning(f"GPT-4o returned a single concept object instead of array. Wrapping in array.")
                        concepts_data = [concepts_data]
                    else:
                        # Log unexpected structure
                        logger.error(f"Unexpected JSON structure from GPT-4o. Keys: {list(concepts_data.keys())}")
                        logger.debug(f"Response content: {content[:500]}")
                        raise Exception(f"Unexpected JSON format from GPT-4o. Expected array or object with 'concepts' key.")

            # Ensure we have a list
            if not isinstance(concepts_data, list):
                logger.error(f"concepts_data is not a list after unwrapping: {type(concepts_data)}")
                raise Exception(f"Expected list of concepts, got {type(concepts_data)}")

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
