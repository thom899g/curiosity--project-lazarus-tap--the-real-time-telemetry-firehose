"""
Firebase Client Module
Manages Firebase initialization and provides Firestore database operations.
Architectural Rationale: Centralizes Firebase interactions, ensures singleton pattern 
for Firebase app, and provides typed operations for Firestore with error handling.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, exceptions
from google.cloud.firestore_v1 import DocumentReference, CollectionReference

from .config import settings

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase client singleton with Firestore operations."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self) -> None: