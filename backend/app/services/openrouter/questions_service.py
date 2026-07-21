import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemini-2.0-flash-exp:free",
)


SYSTEM_PROMPT = """
Tu es un conseiller spécialisé dans l'amélioration de CV.

Tu réponds à partir du CV, de l'offre d'emploi et de l'analyse
de correspondance fournis.

Règles :
- n'invente aucune expérience ni compétence du candidat ;
- distingue les compétences déjà possédées des recommandations ;
- justifie précisément les améliorations proposées ;
- adapte les suggestions à l'offre ;
- tu peux proposer des projets, compétences, formulations
  et améliorations de structure ;
- réponds directement à la question posée.
"""


async def answer_question(
    session: AnalysisSession,
    question: str,
) -> str:
    context = f"""
CV DU CANDIDAT :
{session.cv_text}

OFFRE D'EMPLOI :
{session.offer_text}

ANALYSE DE CORRESPONDANCE :
{session.matching_result.model_dump_json(indent=2)}
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": context,
        },
    ]

    # On ajoute l'historique des précédentes questions.
    messages.extend(
        {
            "role": message.role,
            "content": message.content,
        }
        for message in session.messages
    )

    # Puis la nouvelle question.
    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    answer = response.choices[0].message.content

    if answer is None:
        raise RuntimeError(
            "Le modèle n'a retourné aucune réponse"
        )

    return answer