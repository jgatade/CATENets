"""
Author: Alicia Curth
Utils for transformations
"""
import numpy as onp

HT_TRANSFORMATION = 'HT'
AIPW_TRANSFORMATION = 'AIPW'
RA_TRANSFORMATION = 'RA'

ALL_TRANSFORMATIONS = [HT_TRANSFORMATION, AIPW_TRANSFORMATION, RA_TRANSFORMATION]


def aipw_te_transformation(y, w, p, mu_0, mu_1):
    """
    Transforms data to efficient influence function pseudo-outcome for CATE estimation

    Parameters
    ----------
    y : array-like of shape (n_samples,) or (n_samples, )
        The observed outcome variable
    w: array-like of shape (n_samples,)
        The observed treatment indicator
    p: array-like of shape (n_samples,)
        The treatment propensity, estimated or known. Can be None, then p=0.5 is assumed
    mu_0: array-like of shape (n_samples,)
        Estimated or known potential outcome mean of the control group
    mu_1: array-like of shape (n_samples,)
        Estimated or known potential outcome mean of the treatment group

    Returns
    -------
    d_hat:
        EIF transformation for CATE
    """
    if p is None:
        # assume equal
        p = onp.full(len(y), 0.5)

    w_1 = w / p
    w_0 = (1 - w) / (1 - p)
    return (w_1 - w_0) * y + ((1 - w_1) * mu_1 - (1 - w_0) * mu_0)


def ht_te_transformation(y, w, p, mu_0=None, mu_1=None):
    """
    Transform data to Horvitz-Thompson transformation for CATE

    Parameters
    ----------
    y : array-like of shape (n_samples,) or (n_samples, )
        The observed outcome variable
    w: array-like of shape (n_samples,)
        The observed treatment indicator
    p: array-like of shape (n_samples,)
        The treatment propensity, estimated or known. Can be None, then p=0.5 is assumed
    mu_0: array-like of shape (n_samples,)
        Placeholder, not used. Estimated or known potential outcome mean of the control group
    mu_1: array-like of shape (n_samples,)
        Placerholder, not used. Estimated or known potential outcome mean of the treatment group

    Returns
    -------
    res: array-like of shape (n_samples,)
        Horvitz-Thompson transformed data
    """
    if p is None:
        # assume equal propensities
        p = onp.full(len(y), 0.5)
    return (w / p - (1 - w) / (1 - p)) * y


def ra_te_transformation(y, w, p, mu_0, mu_1):
    """
    Transform data to regression adjustment for CATE

    Parameters
    ----------
    y : array-like of shape (n_samples,) or (n_samples, )
        The observed outcome variable
    w: array-like of shape (n_samples,)
        The observed treatment indicator
    p: array-like of shape (n_samples,)
        Placeholder, not used. The treatment propensity, estimated or known.
    mu_0: array-like of shape (n_samples,)
         Estimated or known potential outcome mean of the control group
    mu_1: array-like of shape (n_samples,)
        Estimated or known potential outcome mean of the treatment group

    Returns
    -------
    res: array-like of shape (n_samples,)
        Regression adjusted transformation
    """
    return w * (y - mu_0) + (1-w) * (mu_1 - y)


TRANSFORMATION_DICT = {HT_TRANSFORMATION: ht_te_transformation,
                       RA_TRANSFORMATION: ra_te_transformation,
                       AIPW_TRANSFORMATION: aipw_te_transformation}


def _get_transformation_function(transformation_name):
    """
    Get transformation function associated with a name
    """
    if transformation_name not in ALL_TRANSFORMATIONS:
        raise ValueError('Parameter first stage should be in '
                         'catenets.models.transformations.ALL_TRANSFORMATIONS.'
                         ' You passed {}'.format(transformation_name))
    return TRANSFORMATION_DICT[transformation_name]
