NEW_SETTINGS = {
    "rankingRules": ["typo", "words"],
    "searchableAttributes": ["title", "overview"],
}

DEFAULT_RANKING_RULES = ["words", "typo", "proximity", "attribute", "sort", "exactness"]

DEFAULT_TYPO_TOLERANCE = {
    "enabled": True,
    "minWordSizeForTypos": {
        "oneTypo": 5,
        "twoTypos": 9,
    },
    "disableOnWords": [],
    "disableOnAttributes": [],
}


def test_get_settings_default(empty_index):
    """Tests getting all settings by default."""
    response = empty_index().get_settings()
    assert isinstance(response, dict)
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response["rankingRules"]
    for typo in DEFAULT_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert typo in response["typoTolerance"]
        assert DEFAULT_TYPO_TOLERANCE[typo] == response["typoTolerance"][typo]
    assert response["distinctAttribute"] is None
    assert response["searchableAttributes"] == ["*"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}


def test_update_settings(empty_index):
    """Tests updating some settings."""
    index = empty_index()
    response = index.update_settings(NEW_SETTINGS)
    assert isinstance(response, dict)
    assert "taskUid" in response
    update = index.wait_for_task(response["taskUid"])
    assert update.status == "succeeded"
    response = index.get_settings()
    for rule in NEW_SETTINGS["rankingRules"]:
        assert rule in response["rankingRules"]
    assert response["distinctAttribute"] is None
    for attribute in NEW_SETTINGS["searchableAttributes"]:
        assert attribute in response["searchableAttributes"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}


def test_reset_settings(empty_index):
    """Tests resetting all the settings to their default value."""
    index = empty_index()
    # Update settings first
    response = index.update_settings(NEW_SETTINGS)
    update = index.wait_for_task(response["taskUid"])
    assert update.status == "succeeded"
    # Check the settings have been correctly updated
    response = index.get_settings()
    for rule in NEW_SETTINGS["rankingRules"]:
        assert rule in response["rankingRules"]
    assert response["distinctAttribute"] is None
    for attribute in NEW_SETTINGS["searchableAttributes"]:
        assert attribute in response["searchableAttributes"]
    assert response["displayedAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}
    # Check the reset of the settings
    response = index.reset_settings()
    assert isinstance(response, dict)
    assert "taskUid" in response
    update = index.wait_for_task(response["taskUid"])
    assert update.status == "succeeded"
    response = index.get_settings()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response["rankingRules"]
    for typo in DEFAULT_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert typo in response["typoTolerance"]
        assert DEFAULT_TYPO_TOLERANCE[typo] == response["typoTolerance"][typo]
    assert response["distinctAttribute"] is None
    assert response["displayedAttributes"] == ["*"]
    assert response["searchableAttributes"] == ["*"]
    assert response["stopWords"] == []
    assert response["synonyms"] == {}
