from RCCServiceSoap import RCCServiceSoap
import logging.config

# https://docs.python-zeep.org/en/latest/transport.html#debugging
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

# create client
client = RCCServiceSoap("127.0.0.1", 64000, 5)
print(client.HelloWorld().HelloWorldResult)