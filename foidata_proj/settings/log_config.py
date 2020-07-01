LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers':{
        '':{
            'handlers':['project', 'mail_admins', 'console'],
            'level':'INFO',
            'propagate': True,
        },
        'django.requests': {
            'handlers': ['project', 'mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'handlers':{
        'project':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':'./logs/project.log',
            'maxBytes': 1024*1024*5, #5mb
            'backupCount': 5,
            'formatter':'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {funcName} {lineno} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
}