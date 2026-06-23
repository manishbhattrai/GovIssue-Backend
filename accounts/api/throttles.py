from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class LoginThrottle(AnonRateThrottle):
    scope = "login"

class RegisterThrottle(AnonRateThrottle):
    scope = "register"

class ProfileUpdateThrottle(UserRateThrottle):
    scope = "profile_update"