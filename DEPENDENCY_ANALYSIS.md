# Dependency Analysis for Experiment Results Extensions

## Current Dependencies Review

### Core Dependencies (Required)
Current `pyproject.toml` dependencies are minimal and well-chosen:

1. **mcp>=1.0.0** - Model Context Protocol framework
   - Status: ✅ Current and suitable
   - Usage: Core MCP server functionality
   - No changes needed

2. **httpx>=0.24.0** - Modern HTTP client
   - Status: ✅ Excellent choice for async HTTP operations
   - Usage: Console API requests, existing Statsig API calls
   - Features we'll use: async support, timeout handling, retry logic
   - No version bump needed

3. **typing-extensions>=4.0.0** - Enhanced type hints
   - Status: ✅ Good for Python 3.10+ compatibility
   - Usage: Advanced type annotations for our new modules
   - No changes needed

### Development Dependencies
Current dev dependencies are comprehensive:
- **pytest>=7.0.0** + **pytest-asyncio>=0.21.0** - Testing framework
- **mypy>=1.0.0** - Type checking
- **ruff>=0.6.0** - Linting and formatting
- **twine>=4.0.0** - Package publishing

## Recommended Additions for Experiment Results

### 1. Caching Dependencies

**Option A: Built-in functools.lru_cache**
- Pros: No additional dependencies, part of stdlib
- Cons: Limited features, memory-only, no TTL support
- Decision: Start with this, upgrade if needed

**Option B: cachetools**
```toml
"cachetools>=5.3.0"  # Advanced caching with TTL, size limits
```
- Pros: TTL support, LRU/LFU policies, size limits
- Cons: Additional dependency
- Recommendation: Add if we need advanced caching features

### 2. Retry Logic Dependencies

**Option A: Built-in tenacity**
```toml
"tenacity>=8.2.0"  # Robust retry library
```
- Pros: Excellent retry strategies, exponential backoff
- Cons: Additional dependency
- Decision: Add this - retry logic is critical for API reliability

**Option B: Custom implementation**
- Pros: No dependencies
- Cons: More code to maintain, less battle-tested
- Decision: Avoid - tenacity is well-established

### 3. Data Processing Dependencies

**Option A: No additional dependencies**
- Use built-in json, csv modules
- Pros: No additional dependencies
- Cons: Limited data manipulation capabilities

**Option B: Add pandas (NOT recommended)**
```toml
"pandas>=2.0.0"  # Heavy dependency for simple CSV export
```
- Pros: Powerful data manipulation
- Cons: Large dependency, overkill for our needs
- Decision: Avoid - use stdlib

### 4. Async Utilities

**asyncio-throttle** (Optional)
```toml
"asyncio-throttle>=1.1.0"  # Rate limiting for async requests
```
- Pros: Clean async rate limiting
- Cons: Can implement ourselves with asyncio
- Decision: Implement basic rate limiting ourselves first

## Final Recommended Dependencies

### Immediate Additions (Step 3-5)
```toml
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.24.0", 
    "typing-extensions>=4.0.0",
    "tenacity>=8.2.0",  # NEW: Retry logic for API calls
]
```

### Future Additions (Step 10-11)
```toml
# If advanced caching is needed:
"cachetools>=5.3.0",

# If we need structured logging:
"structlog>=23.1.0",
```

### Development Dependencies Additions
```toml
dev = [
    # ... existing dev dependencies ...
    "httpx-mock>=0.11.0",     # NEW: Mock HTTP requests for testing
    "freezegun>=1.2.0",       # NEW: Time-based testing for caching
]
```

## Dependency Strategy by Implementation Step

### Steps 3-5: Console API Integration
- **Add**: `tenacity>=8.2.0` for retry logic
- **Use existing**: `httpx` for HTTP requests
- **Use stdlib**: `asyncio` for concurrency, `functools.lru_cache` for basic caching

### Steps 6-9: MCP Tools Implementation  
- **No new dependencies**: Use existing MCP framework and HTTP client
- **Use stdlib**: `json` for response formatting, `csv` for basic exports

### Steps 10-11: Error Handling and Caching
- **Consider adding**: `cachetools>=5.3.0` if stdlib caching is insufficient
- **Use existing**: `tenacity` for comprehensive error handling

### Steps 12-15: Testing and Documentation
- **Add dev dependencies**: `httpx-mock`, `freezegun` for better testing
- **No new runtime dependencies**

## Risk Assessment

### Low Risk Dependencies
- **tenacity**: Mature, stable, focused single purpose
- **cachetools**: Mature, lightweight, optional

### Dependencies to Avoid
- **pandas**: Too heavy for simple CSV export
- **requests**: We already have httpx (async)
- **redis/memcached clients**: Overkill for our caching needs

## Version Pinning Strategy

### Production Dependencies
- Use minimum viable versions with `>=` to allow updates
- Pin exact versions only if compatibility issues arise

### Development Dependencies  
- Use `>=` for flexibility during development
- Consider exact pinning in CI/CD for reproducible builds

## Migration Path

### Phase 1 (Steps 3-5): Minimal additions
```bash
# Add to pyproject.toml
pip install tenacity>=8.2.0
```

### Phase 2 (Steps 10-11): Performance optimization
```bash
# Only if needed based on performance testing
pip install cachetools>=5.3.0
```

### Phase 3 (Steps 12-15): Testing enhancement
```bash
# Add to dev dependencies
pip install httpx-mock>=0.11.0 freezegun>=1.2.0
```

## Summary

The current dependency foundation is excellent. We recommend:

1. **Immediate**: Add `tenacity` for robust retry logic
2. **Conditional**: Add `cachetools` only if stdlib caching proves insufficient  
3. **Testing**: Add `httpx-mock` and `freezegun` for comprehensive testing
4. **Avoid**: Heavy dependencies like pandas, redis clients, or requests

This approach maintains the project's lightweight philosophy while adding essential reliability features for production API integrations.
