return iif($feature.AuthorizationType == 'NO', {
    'errorMessage': 'AuthorizationType may not be Unauthorized (NO); select the appropriate value from the UICAuthorizeTypeDomain (dropdown menu).'
}, true);
