

# Roles package initialization
# This will contain all the specialized agent roles

from .product_manager import ProductManager
from .architect import Architect
from .engineer import Engineer
from .qa_engineer import QaEngineer
from .librarian import LibrarianAgent

__all__ = ['ProductManager', 'Architect', 'Engineer', 'QaEngineer', 'LibrarianAgent']

