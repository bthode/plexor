def test_sum():
    assert 2 + 2 == 4


'''
Tests:
Videos are added as pending|excluded per the retention policy
* Pending
* Excluded

Videos go from complete to excluded based on their retention policy

Excluded videos are deleted OR never downloaded to start with

Complete videos are not act acted upon

Create database creates the database correctly

Delete database deletes it



'''
