django.jQuery(document).ready(function() {
    django.jQuery('#id_entity_content_type').change(function(event) {
        // ID of the ContentType instance
        const conttenttypeId = event.target.value

        window.open(
            `/contenttype_object/${conttenttypeId}/`,"","width=900,height=700"
        )
    })
})

function getId(id) {
    window.opener.document.getElementById('id_entity_object_id').value = id
    window.close()
}
