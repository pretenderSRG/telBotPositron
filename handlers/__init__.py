from .common import router as common_router
from .fallback import router as fallback_router
from .gpt import router as gpt_router
from .celebrity_talk import router as celebrity_talk_router
from .quiz import router as quiz_router
from .random_fact import router as random_fact_router
from .recommend import router as recommend_router
from .gym import router as gym_router

routers = [
    celebrity_talk_router,
    common_router,
    gpt_router,
    quiz_router,
    random_fact_router,
    gym_router,
    recommend_router,
    fallback_router,  # завжди останній: ловить усе, що не зловили інші
]