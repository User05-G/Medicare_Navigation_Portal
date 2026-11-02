/**
 * REST API client service for communicating with Flask Backend.
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Fetch all 18 hospital locations.
 */
export async function fetchLocations() {
  try {
    const response = await fetch(`${API_BASE_URL}/locations`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch locations:', error);
    throw error;
  }
}

/**
 * Perform Default Reasoning on a user query string.
 */
export async function performReasoning(query) {
  try {
    const response = await fetch(`${API_BASE_URL}/reason`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    return await response.json();
  } catch (error) {
    console.error('Reasoning API error:', error);
    throw error;
  }
}

/**
 * Execute Direct Navigation.
 */
export async function navigateDirect(start, destination, algorithm = 'astar') {
  try {
    const response = await fetch(`${API_BASE_URL}/navigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, destination, algorithm })
    });
    return await response.json();
  } catch (error) {
    console.error('Direct navigation API error:', error);
    throw error;
  }
}

/**
 * Execute Intelligent Navigation (Default Reasoning + Route Search).
 */
export async function navigateIntelligent(start, query, algorithm = 'astar') {
  try {
    const response = await fetch(`${API_BASE_URL}/intelligent-navigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, query, algorithm })
    });
    return await response.json();
  } catch (error) {
    console.error('Intelligent navigation API error:', error);
    throw error;
  }
}

/**
 * Perform side-by-side BFS vs A* algorithm comparison.
 */
export async function compareAlgorithms(start, destination) {
  try {
    const response = await fetch(`${API_BASE_URL}/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, destination })
    });
    return await response.json();
  } catch (error) {
    console.error('Compare API error:', error);
    throw error;
  }
}
