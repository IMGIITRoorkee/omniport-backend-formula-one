django.jQuery(document).ready(function() {
    django.jQuery('#id_entity_content_type').change(function(event) {
        const conttenttypeId = event.target.value
        const entityContentObject = '#id_entity_content_object'
        django.jQuery(entityContentObject).html('')
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
