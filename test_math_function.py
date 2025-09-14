


"""
Test file for math function problem
"""

def test_add_function():
    """Test the add function"""
    # This should be implemented by the problem solver
    try:
        from solution import add
        result = add(2, 3)
        assert result == 5, f"Expected 5, got {result}"
        print("✅ Add function test passed")
        return True
    except ImportError:
        print("❌ Add function not implemented")
        return False
    except AssertionError as e:
        print(f"❌ Add function test failed: {e}")
        return False

if __name__ == "__main__":
    test_add_function()


