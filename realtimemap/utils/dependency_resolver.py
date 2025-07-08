from contextlib import asynccontextmanager


@asynccontextmanager
async def resolve_dependency(gen_func, *args, **kwargs):
    """Адаптер для преобразования генераторных зависимостей в контекстные менеджеры"""
    gen = gen_func(*args, **kwargs)
    try:
        dependency = await gen.__anext__()
        yield dependency
    except StopAsyncIteration:
        pass
    finally:
        try:
            await gen.__anext__()
        except StopAsyncIteration:
            pass
