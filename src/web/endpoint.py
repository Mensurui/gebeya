from fastapi import APIRouter, Depends
#from fastapi.templating import Jinja2Template
from ..model import schema
from sqlalchemy.ext.asyncio import AsyncSession
from ..data.dependency import get_db
from ..service import service, oauth2
from typing import List

router = APIRouter()

@router.post("/admin")
async def add_admin(admin_data:schema.AdminRegister, db:AsyncSession=Depends(get_db)):
    admin_values = await service.register_admin(admin_data=admin_data, db=db)
    return admin_values
@router.post("/add_supplier")
async def add_supplier(supplier_data:schema.SupplierRegister, db:AsyncSession=Depends(get_db), admin=Depends(oauth2.get_admin)):
    admin_username = admin
    supplier_values = await service.register_supplier(admin_username=admin_username, supplier_data=supplier_data, db=db)
    return supplier_values
@router.post("/add_category")
async def add_category(category_data:schema.CategoryBase, db:AsyncSession=Depends(get_db), admin=Depends(oauth2.get_admin)):
    admin_username = admin
    category_values = await service.register_category(admin_username=admin_username, category_data=category_data, db=db)
    return category_values
@router.post("/add_item")
async def add_item(item_data:schema.ItemRegister, db:AsyncSession=Depends(get_db), admin=Depends(oauth2.get_admin)):
    admin_username = admin
    item_values = await service.register_item(admin_username=admin_username, item_data=item_data, db=db)
    return item_values
@router.post("/add_selling_price")
async def add_selling_price(selling_data:schema.SellingRegister, db:AsyncSession=Depends(get_db), admin=Depends(oauth2.get_admin)):
    admin_username=admin
    selling_value = await service.register_selling_price(admin_username=admin_username, selling_data=selling_data, db=db)
    return selling_value
@router.post("/add_transaction")
async def add_transaction(transaction_data:schema.TransactionRegister, db:AsyncSession=Depends(get_db), admin=Depends(oauth2.get_admin)):
    admin_username=admin
    transaction_value = await service.register_transaction(admin_username=admin_username, transaction_data=transaction_data, db=db)
    return transaction_value

@router.get("/get_items", response_model=List[schema.ItemUserOut])
async def get_items(db:AsyncSession=Depends(get_db)):
    items_list = await service.items(db=db)
    print(f"Items:{items_list}")
    return items_list
