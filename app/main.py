from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.router import inventory, warehouse, category, product, supplier, purchase_order, stock_receipt, stock_movement, department, staff, service, customer
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
# Import all models to ensure SQLAlchemy metadata is properly registered
from app.models import Department, Staff, Service, Customer

app = FastAPI(
    title="Ecosphere Inventory API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

#app.add_middleware(SlowAPIMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all HTTP headers.
)
@app.get("/api/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"})

app.include_router(inventory.router, prefix="/api", tags=["inventory"])
app.include_router(warehouse.router, prefix="/api", tags=["warehouse"])
app.include_router(category.router, prefix="/api", tags=["category"])
app.include_router(product.router, prefix="/api", tags=["product"])
app.include_router(supplier.router, prefix="/api", tags=["supplier"])
app.include_router(purchase_order.router, prefix="/api", tags=["purchase-order"])
app.include_router(stock_receipt.router, prefix="/api", tags=["stock-receipt"])
app.include_router(stock_movement.router, prefix="/api", tags=["stock-movement"])
app.include_router(department.router, prefix="/api", tags=["department"])
app.include_router(staff.router, prefix="/api", tags=["staff"])
app.include_router(service.router, prefix="/api", tags=["service"])
app.include_router(customer.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Ecosphere Inventory API"} 