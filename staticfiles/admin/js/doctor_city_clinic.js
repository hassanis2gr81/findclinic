(function($) {
    $(document).ready(function() {
        // elements
        const $city = $('#id_city');
        // inline clinic selects end with "-clinic" in their id (e.g. id_form-0-clinic)
        // but sometimes you may also have a master #id_clinics (if you used M2M)
        const $masterClinics = $('#id_clinics');

        // Initialize Select2 for master clinics if present
        if ($.fn.select2 && $masterClinics.length) {
            $masterClinics.select2({
                multiple: true,
                width: '100%',
                placeholder: 'Select clinic(s)'
            });
        }

        if ($.fn.select2 && $city.length) {
            $city.select2({ width: '100%' });
        }

        // function to populate a given <select> with clinic options
        function populateSelect($select, data, keepValue) {
            const current = keepValue ? $select.val() : null;
            $select.empty();
            if (!$select.is(':disabled')) {
                $select.append(new Option('---------', '')); // default blank
            }
            data.forEach(function(clinic) {
                const option = new Option(clinic.name, clinic.id, false, false);
                $select.append(option);
            });
            if (keepValue && current) {
                $select.val(current);
            }
            $select.trigger('change');
        }

        // When city changes: fetch clinics and populate inline selects & master select
        $city.on('change', function() {
            const cityId = $(this).val();
            if (!cityId) {
                // clear master select
                if ($masterClinics.length) {
                    populateSelect($masterClinics, []);
                }
                // clear inline selects
                $('select[id$="-clinic"]').each(function() {
                    populateSelect($(this), [], false);
                });
                return;
            }

            $.ajax({
                url: '/ajax/load-clinics/',
                data: { 'city': cityId },
                dataType: 'json',
                success: function(data) {
                    // populate master clinics select if exists
                    if ($masterClinics.length) {
                        populateSelect($masterClinics, data, false);
                    }
                    // populate all inline clinic selects (tabular inline / stacked inline)
                    $('select[id$="-clinic"]').each(function() {
                        populateSelect($(this), data, true); // keep current if exists
                    });
                },
                error: function(xhr, status, error) {
                    console.error("Error loading clinics:", error);
                }
            });
        });

        // When new inline row is added, ensure its clinic select is populated with current city's clinics
        $(document).on('formset:added', function(event, $row, formsetName) {
            // $row is the newly added inline row
            const $newClinicSelect = $row.find('select[id$="-clinic"]');
            if ($newClinicSelect.length) {
                // trigger city change to populate it
                $city.trigger('change');
            }
            // init flatpickr on new time inputs
            if (typeof flatpickr !== "undefined") {
                $row.find('input[name$="start_time"], input[name$="end_time"]').flatpickr({
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    time_24hr: true
                });
            }
        });

        // initialize flatpickr for existing inline rows on page load
        if (typeof flatpickr !== "undefined") {
            $('input[name$="start_time"], input[name$="end_time"]').flatpickr({
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i",
                time_24hr: true
            });
        }
    });
})(django.jQuery);
