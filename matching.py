import pandas as pd
import numpy as np
from openai import OpenAI
from typing import List, Dict, Tuple
import os
from sklearn.metrics.pairwise import cosine_similarity
import logging

class SemanticMatcher:
    def __init__(self, api_key: str = None):
        """
        Initialize the SemanticMatcher with OpenAI API key.
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment variables.
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key is None:
                raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        self.client = OpenAI(api_key=api_key)
        self.embedding_cache = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a text string using OpenAI's API.
        Implements caching to avoid redundant API calls.
        
        Args:
            text: Text to get embedding for
            
        Returns:
            List of embedding values
        """
        # Check cache first
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding
            # Cache the result
            self.embedding_cache[text] = embedding
            return embedding
        except Exception as e:
            self.logger.error(f"Error getting embedding for text '{text}': {str(e)}")
            raise

    def find_matches(self, 
                    supply_items: pd.DataFrame, 
                    demand_items: pd.DataFrame,
                    similarity_threshold: float = 0.8,
                    max_matches: int = 3) -> List[Dict]:
        """
        Find semantic matches between supply and demand items.
        
        Args:
            supply_items: DataFrame with columns 'SupplyItemName' and 'Quantity'
            demand_items: DataFrame with columns 'DemandItemName' and 'Quantity'
            similarity_threshold: Minimum cosine similarity score to consider a match
            max_matches: Maximum number of matches to return for each demand item
            
        Returns:
            List of dictionaries containing matches and their details
        """
        # Get embeddings for all items
        supply_embeddings = np.array([
            self.get_embedding(name) for name in supply_items['SupplyItemName']
        ])
        
        demand_embeddings = np.array([
            self.get_embedding(name) for name in demand_items['DemandItemName']
        ])
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(demand_embeddings, supply_embeddings)
        
        matches = []
        
        # Find matches for each demand item
        for i, demand_row in demand_items.iterrows():
            demand_name = demand_row['DemandItemName']
            demand_quantity = demand_row['Quantity']
            
            # Get similarity scores for this demand item
            similarity_scores = similarity_matrix[i]
            
            # Get indices of top matches above threshold
            top_indices = np.where(similarity_scores >= similarity_threshold)[0]
            top_indices = top_indices[np.argsort(similarity_scores[top_indices])[-max_matches:]]
            
            for idx in top_indices:
                supply_name = supply_items.iloc[idx]['SupplyItemName']
                supply_quantity = supply_items.iloc[idx]['Quantity']
                similarity_score = similarity_scores[idx]
                
                matches.append({
                    'demand_item': demand_name,
                    'demand_quantity': demand_quantity,
                    'supply_item': supply_name,
                    'supply_quantity': supply_quantity,
                    'similarity_score': similarity_score
                })
        
        # Sort matches by similarity score
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches

    