from pydantic import BaseModel

class AdminRegister(BaseModel):
    username:str
    password:str

class AdminOut(BaseModel):
    username:str
    class Config:
        from_attributes=True

class SupplierRegister(BaseModel):
    supplier_name:str
    supplier_address:str
    supplier_phonenumber:str

class SupplierOut(SupplierRegister):
    class Config:
        from_attributes=True

class CategoryBase(BaseModel):
    category_name:str

class CategoryOut(CategoryBase):
    class Config:
        from_attributes=True

class ItemBase(BaseModel):
    item_name:str
    item_price:float
    item_count:int

class ItemRegister(ItemBase):
    supplier_id:int
    category_id:int

class ItemOut(ItemBase):
    class Config:
        from_attributes=True

class SellingBase(BaseModel):
    selling_price:float

class SellingRegister(SellingBase):
    item_id: int

class SellingOut(SellingBase):
    item_name:str
    class Config:
        from_attributes=True

class TransactionBase(BaseModel):
    sold_to:str
    sold_amount:float

class TransactionRegister(TransactionBase):
    item_id:int

class TransactionOut(TransactionBase):
    item_name:str
    class Config:
        from_attributes=True

class ItemWarehouseRegister(BaseModel):
    item_id:int
    supplier:int
    current_amount:int

class ItemWarehouseOut(BaseModel):
    item_name:str
    supplier_name:str
    current_amount:str

class ItemUserOut(BaseModel):
    item_name:str
    category_name:str
    selling_price:float
