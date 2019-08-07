if (!haskey($feature, 'USDWContamination') || isempty($feature.USDWContamination)) {
    return;
}

if (lower(domainname($feature, 'USDWContamination')) != 'yes') {
    return;
}

return 'Y';
