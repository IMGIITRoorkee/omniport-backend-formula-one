django.jQuery(document).ready(function() {
    django.jQuery('#id_entity_content_type').change(function(event) {
        // ID of the ContentType instance
        const conttenttypeId = event.target.value
        // ID of the dropdown list to be populated
        const entityContentObject = '#id_entity_content_object'
        // Reset list on change of ContentType instance
        django.jQuery(entityContentObject).html('')

        // GET request to fetch all objects in the ContentType instance
        django.jQuery.ajax({
            type: 'GET',
            url: `/contenttype_object/${conttenttypeId}/`,
            success: function(data) {                
                django.jQuery.each(data, function(_, obj) {
                    django.jQuery('<option/>').val(obj.value).text(obj.label)
                    .appendTo(entityContentObject)
                })
            },
        })
    })
})
