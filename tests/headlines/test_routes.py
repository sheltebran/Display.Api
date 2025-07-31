import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from features.headlines.routes import router
from features.headlines.models import HeadlineDto
from datetime import datetime

# Create a test client
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Test data
TEST_HEADLINE_DTOS = [
    HeadlineDto(
        heading="Test Headline 1",
        story="Test story 1",
        link="https://example.com/story1",
        pub_date=datetime(2024, 1, 1, 12, 0, 0),
        league_id=1
    ),
    HeadlineDto(
        heading="Test Headline 2",
        story="Test story 2",
        link="https://example.com/story2",
        pub_date=datetime(2024, 1, 2, 12, 0, 0),
        league_id=1
    )
]

def test_create_headlines_invalid_sport_id():
    """Test create headlines with invalid sport ID"""
    # Act
    response = client.post("/headlines/invalid")

    # Assert
    # FastAPI returns 404 for path parameter type mismatches
    assert response.status_code == 404

def test_list_headlines_invalid_league_id():
    """Test list headlines with invalid league ID"""
    # Act
    response = client.get("/headlines/invalid")

    # Assert
    # FastAPI returns 404 for path parameter type mismatches
    assert response.status_code == 404

def test_route_structure():
    """Test that routes are properly configured"""
    # This test verifies the route structure exists
    routes = [route for route in app.routes if hasattr(route, 'path')]
    route_paths = [route.path for route in routes]

    # Check that we have headlines routes
    headlines_routes = [path for path in route_paths if "/headlines/" in path]
    assert len(headlines_routes) >= 1  # At least one headlines route should exist

    # Check that we have both GET and POST methods available
    routes_with_methods = [route for route in app.routes if hasattr(route, 'methods')]
    has_post = any('POST' in route.methods for route in routes_with_methods)
    has_get = any('GET' in route.methods for route in routes_with_methods)

    assert has_post, "Should have POST routes"
    assert has_get, "Should have GET routes"