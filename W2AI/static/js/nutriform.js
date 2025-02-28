document.addEventListener('DOMContentLoaded', function() {
    // Plot data passed from the backend
    const plotsData = [
        {% for plot in plots %}
            {
                name: "{{ plot.plot_name }}",
                crop: "{{ plot.crop_grown }}",
                area: "{{ plot.land_area }}",
                soilCondition: "{{ plot.soil_condition }}",
                soilHealth: "{{ plot.soil_health }}",
                soilPH: "{{ plot.soil_ph }}",
                waterSource: "{{ plot.water_source }}",
                waterAvail: "{{ plot.water_availability }}",
                richNutrients: "{{ plot.soil_rich_nutrients }}",
                averageNutrients: "{{ plot.soil_average_nutrients }}",
                poorNutrients: "{{ plot.soil_poor_nutrients }}"
            },
        {% endfor %}
    ];
    
    // Add event listeners to plot radio buttons
    const plotRadios = document.querySelectorAll('input[name="plot"]');
    plotRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const selectedPlotName = this.value;
            
            // For new plot selection, clear all fields
            if (selectedPlotName === 'new_plot') {
                document.getElementById('id_plot_name').value = '';
                document.getElementById('id_land_area').value = '';
                clearSelectValues(['id_crop_grown', 'id_soil_condition', 'id_soil_health', 'id_soil_ph',
                                  'id_water_source', 'id_water_availability', 'id_soil_rich_nutrients',
                                  'id_soil_average_nutrients', 'id_soil_poor_nutrients']);
                return;
            }
            
            const selectedPlot = plotsData.find(plot => plot.name === selectedPlotName);
            
            if (selectedPlot) {
                // Populate form fields with plot data
                document.getElementById('id_plot_name').value = selectedPlot.name;
                
                // Set select values
                setSelectValue('id_crop_grown', selectedPlot.crop);
                document.getElementById('id_land_area').value = selectedPlot.area;
                setSelectValue('id_soil_condition', selectedPlot.soilCondition);
                setSelectValue('id_soil_health', selectedPlot.soilHealth);
                setSelectValue('id_soil_ph', selectedPlot.soilPH);
                setSelectValue('id_water_source', selectedPlot.waterSource);
                setSelectValue('id_water_availability', selectedPlot.waterAvail);
                setSelectValue('id_soil_rich_nutrients', selectedPlot.richNutrients);
                setSelectValue('id_soil_average_nutrients', selectedPlot.averageNutrients);
                setSelectValue('id_soil_poor_nutrients', selectedPlot.poorNutrients);
            }
        });
    });
    
    // Helper function to set select values
    function setSelectValue(selectId, value) {
        const selectElement = document.getElementById(selectId);
        if (selectElement && value) {
            for (let i = 0; i < selectElement.options.length; i++) {
                if (selectElement.options[i].value === value) {
                    selectElement.selectedIndex = i;
                    break;
                }
            }
        }
    }
    
    // Helper function to clear select values
    function clearSelectValues(selectIds) {
        selectIds.forEach(id => {
            const selectElement = document.getElementById(id);
            if (selectElement) {
                selectElement.selectedIndex = 0;
            }
        });
    }
    
    // Handle fertilizer formset
    const formsetContainer = document.getElementById('fertilizer-formset');
    const addButton = document.getElementById('add-fertilizer');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
    
    // Initialize formset count
    let formCount = 0;
    
    // Extract the template form from existing formset or create a template
    let templateForm = '';
    
    {% if fertilizer_formset.forms %}
        // Get the first form as template
        {% with form=fertilizer_formset.forms.0 %}
            templateForm = `
                <div class="fertilizer-form">
                    <h6>Fertilizer #__COUNT__</h6>
                    <div class="fertilizer-form-fields">
                        {% for field in form %}
                            <div class="form-group">
                                <label for="{{ field.id_for_label }}">{{ field.label }}:</label>
                                {{ field }}
                                {% if field.errors %}
                                    <div class="invalid-feedback">{{ field.errors.0 }}</div>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                    <button type="button" class="remove-fertilizer btn btn-sm btn-danger">Remove</button>
                </div>
            `;
        {% endwith %}
    {% else %}
        // Create a generic template if no forms exist
        templateForm = `
            <div class="fertilizer-form">
                <h6>Fertilizer #__COUNT__</h6>
                <div class="fertilizer-form-fields">
                    <p>No fertilizer form template available. Please check your formset configuration.</p>
                </div>
            </div>
        `;
    {% endif %}
    
    // Function to add a new fertilizer form
    function addFertilizerForm() {
        // Clone from template
        let newForm = templateForm.replace('__COUNT__', formCount + 1);
        
        // Update form index in all fields
        newForm = newForm
            .replace(/-0-/g, `-${formCount}-`)
            .replace(/_0_/g, `_${formCount}_`);
        
        // Add to container
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newForm;
        const formElement = tempDiv.firstElementChild;
        
        // Clear input values for new forms (except hidden fields)
        if (formCount > 0) {
            formElement.querySelectorAll('input:not([type="hidden"]), select, textarea').forEach(input => {
                input.value = '';
                if (input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                }
            });
        }
        
        // Add remove button functionality
        const removeButton = formElement.querySelector('.remove-fertilizer');
        if (removeButton) {
            removeButton.addEventListener('click', function() {
                formElement.remove();
                updateFormCount();
            });
        }
        
        formsetContainer.appendChild(formElement);
        
        // Update form count
        formCount++;
        updateFormCount();
        
        return formElement;
    }
    
    // Function to update the total forms count
    function updateFormCount() {
        if (totalForms) {
            // Get the current number of forms in the DOM
            const currentFormCount = document.querySelectorAll('.fertilizer-form').length;
            totalForms.value = currentFormCount;
        }
    }
    
    // Add fertilizer form when button is clicked
    addButton.addEventListener('click', addFertilizerForm);
    
    // Add initial fertilizer form if none exists
    if (formsetContainer.children.length === 0) {
        addFertilizerForm();
    } else {
        // If forms already exist, update the form count
        formCount = formsetContainer.children.length;
        updateFormCount();
        
        // Add remove buttons to existing forms
        document.querySelectorAll('.fertilizer-form').forEach((form, index) => {
            if (index > 0) {  // Keep at least one form
                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'remove-fertilizer btn btn-sm btn-danger';
                removeBtn.textContent = 'Remove';
                removeBtn.addEventListener('click', function() {
                    form.remove();
                    updateFormCount();
                });
                form.appendChild(removeBtn);
            }
        });
    }
    
    // Form validation
    const form = document.getElementById('farmerPurchaseForm');
    form.addEventListener('submit', function(event) {
        // Enable console logging to debug form submission
        console.log("Attempting to submit form...");
        
        // Validate required fields
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
                // Add error message near the field
                let errorMsg = field.nextElementSibling;
                if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'invalid-feedback';
                    field.parentNode.insertBefore(errorMsg, field.nextSibling);
                }
                errorMsg.textContent = 'This field is required.';
                
                // Scroll to the first error
                if (field === requiredFields[0]) {
                    field.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                field.classList.remove('is-invalid');
                // Remove error message if it exists
                const errorMsg = field.nextElementSibling;
                if (errorMsg && errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg.textContent = '';
                }
            }
        });
        
        // Check if Other Irrigation method is provided when needed
        const irrigationMethod = document.getElementById('id_irrigation_method').value;
        const otherIrrigation = document.getElementById('id_other_irrigation');
        
        if (irrigationMethod === 'Other Irrigation Method' && !otherIrrigation.value.trim()) {
            otherIrrigation.classList.add('is-invalid');
            let errorMsg = otherIrrigation.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                otherIrrigation.parentNode.insertBefore(errorMsg, otherIrrigation.nextSibling);
            }
            errorMsg.textContent = 'Please specify the other irrigation method.';
            isValid = false;
        }
        
        // Check if at least one fertilizer form exists
        const fertilizerForms = document.querySelectorAll('.fertilizer-form');
        if (fertilizerForms.length === 0) {
            isValid = false;
            alert('Please add at least one fertilizer information!');
            document.getElementById('add-fertilizer').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Validate all fertilizer forms have required fields filled
        fertilizerForms.forEach((formElem, idx) => {
            const requiredFertilizerFields = formElem.querySelectorAll('[required]');
            requiredFertilizerFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                        errorMsg = document.createElement('div');
                        errorMsg.className = 'invalid-feedback';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                    errorMsg.textContent = `Required for Fertilizer #${idx + 1}`;
                }
            });
        });
        
        if (!isValid) {
            event.preventDefault();
            console.log("Form validation failed");
            alert('Please fill all required fields!');
        } else {
            console.log("Form validation successful, submitting...");
            // Log form data for debugging
            const formData = new FormData(form);
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }
        }
    });
    
    // Toggle other irrigation field visibility
    function toggleOtherIrrigation() {
        const irrigationMethod = document.getElementById('id_irrigation_method').value;
        const otherIrrigationDiv = document.getElementById('other_irrigation_div');
        const otherIrrigationInput = document.getElementById('id_other_irrigation');
        
        if (irrigationMethod === 'Other Irrigation Method') {
            otherIrrigationDiv.style.display = 'block';
            otherIrrigationInput.setAttribute('required', 'required');
        } else {
            otherIrrigationDiv.style.display = 'none';
            otherIrrigationInput.removeAttribute('required');
            otherIrrigationInput.value = '';
        }
    }
    
    // Call toggleOtherIrrigation on page load to set initial state
    toggleOtherIrrigation();
    
    // Also attach the function to the irrigation method dropdown change event
    document.getElementById('id_irrigation_method').addEventListener('change', toggleOtherIrrigation);
});
