#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `aionest` package."""
import pytest

from aionest import NestApi


def test_init():
    """Test init."""
    nest_api = NestApi(product_id="product-id")
    assert nest_api is not None

    nest_api = NestApi("product-id", access_token="access-token")
    assert nest_api is not None
