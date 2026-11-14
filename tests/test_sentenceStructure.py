from src.sentenceStructure import contractionsBreakdown
import pytest

def testContractions():
    t = contractionsBreakdown("don't")
    assert(t[0].base == "do")
    assert(t[1].base == "not")