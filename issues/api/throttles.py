from rest_framework.throttling import UserRateThrottle

class UpdateIssueThrottle(UserRateThrottle):
    scope = "issue_update"