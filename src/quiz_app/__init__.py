"""Quiz Application - A dynamic timer-based quiz system."""

__version__ = "0.1.0"
__author__ = "Zishan Paya"

from .core import Quiz, QuizLoader, LoadQuestion
from .cli import main

__all__ = ["Quiz", "QuizLoader", "LoadQuestion", "main"] 