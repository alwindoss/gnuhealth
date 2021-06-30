try:
    from trytond.modules.health_dentistry.tests.test_health_dentistry \
        import suite
except ImportError:
    from .test_health_dentistry import suite

__all__ = ['suite']
