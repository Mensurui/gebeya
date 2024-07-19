from ..model import schema, model
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..data.dependency import get_db
from . import utils
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

async def register_admin(admin_data:schema.AdminRegister, db:AsyncSession=Depends(get_db)):
    db_adminre = model.Admin(**admin_data.dict())
    db_adminre.password = utils.get_hash(db_adminre.password)
    db.add(db_adminre)
    await db.commit()
    await db.refresh(db_adminre)
    return db_adminre

async def register_supplier(admin_username:str, supplier_data:schema.SupplierRegister, db:AsyncSession=Depends(get_db)):
    admin = await db.execute(select(model.Admin).where(model.Admin.username == admin_username))
    admin_data = admin.scalar()
    if not admin_data:
        raise HTTPExcpetion(status=404, detail=f"Unauthenticated")
    db_supre = model.Supplier(**supplier_data.dict())
    db.add(db_supre)
    await db.commit()
    await db.refresh(db_supre)
    return db_supre

async def register_category(admin_username:str, category_data:schema.CategoryBase, db:AsyncSession=Depends(get_db)):
    admin = await db.execute(select(model.Admin).where(model.Admin.username == admin_username))
    admin_data = admin.scalar()
    if not admin_data:
        raise HTTPExcpetion(status=404, detail=f"Unauthenticated")

    db_catgre = model.Category(**category_data.dict())
    db.add(db_catgre)
    await db.commit()
    await db.refresh(db_catgre)
    return db_catgre

async def register_item(admin_username:str, item_data:schema.ItemRegister, db:AsyncSession=Depends(get_db)):
    admin = await db.execute(select(model.Admin).where(model.Admin.username == admin_username))
    admin_data = admin.scalar()
    if not admin_data:
        raise HTTPExcpetion(status=404, detail=f"Unauthenticated")

    db_itemre = model.Item(**item_data.dict())
    db.add(db_itemre)
    await db.commit()
    await db.refresh(db_itemre)

    db_itemwar = model.ItemWarehouse(
            item_id = db_itemre.id,
            supplier_id = db_itemre.supplier_id,
            current_amount = db_itemre.item_count
            )
    db.add(db_itemwar)
    await db.commit()
    await db.refresh(db_itemwar)
    return db_itemre

async def register_selling_price(admin_username:str, selling_data:schema.SellingRegister, db:AsyncSession=Depends(get_db)):
    admin = await db.execute(select(model.Admin).where(model.Admin.username == admin_username))
    admin_data = admin.scalar()
    if not admin_data:
        raise HTTPExcpetion(status=404, detail=f"Unauthenticated")
    db_sellre = model.Selling(**selling_data.dict())
    db.add(db_sellre)
    await db.commit()
    await db.refresh(db_sellre)
    return db_sellre

async def register_transaction(admin_username:str, transaction_data:schema.TransactionRegister, db:AsyncSession=Depends(get_db)):
    admin = await db.execute(select(model.Admin).where(model.Admin.username == admin_username))
    admin_data = admin.scalar()
    if not admin_data:
        raise HTTPExcpetion(status=404, detail=f"Unauthenticated")
    db_trare = model.Transaction(**transaction_data.dict())
    db.add(db_trare)
    await db.commit()
    await db.refresh(db_trare)
    db_itemwarquery = await db.execute(select(model.ItemWarehouse).where(model.ItemWarehouse.item_id == transaction_data.item_id))
    db_itemwar = db_itemwarquery.scalar()
    total_amount = db_itemwar.current_amount - db_trare.sold_amount
    db_itemwar.current_amount = total_amount
    db.add(db_itemwar)
    await db.commit()
    await db.refresh(db_itemwar)
    return db_trare

async def items(db: AsyncSession = Depends(get_db)):
    items_query = select(model.Item).options(joinedload(model.Item.category), joinedload(model.Item.selling))
    items_data = await db.execute(items_query)
    curated_items = [
        schema.ItemUserOut(
            item_name=item_data.item_name,
            category_name=item_data.category.category_name,
            selling_price=item_data.selling.selling_price,
        )
        for item_data in items_data.scalars().all()
    ]
    return curated_items

