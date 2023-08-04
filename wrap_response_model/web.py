from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from wrap_response_model.wrap_resp import wrap_model

router = APIRouter()


class Item(BaseModel):
    item_id: int


@router.get("/")
def read_root():
    return {"Hello": "World"}

# router.xxx 里不得再使用 response_model 参数
@router.get("/items/1")
@wrap_model  # wrap_model 一定要放在 @router.xxx 装饰器之下
async def read_item() -> Item:  # 这里一定要申明返回值的类型
    return {"item_id": 1}


app = FastAPI()
app.include_router(router)
