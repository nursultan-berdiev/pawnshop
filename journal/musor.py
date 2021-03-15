
def save_loan_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            loans = Loan.objects.all()
            data['html_loan_list'] = render_to_string('journal/index.html', {'loans': loans})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
    else:
        form = LoanForm()
    return save_loan_form(request, form, 'journal/product_form.html')


def update_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
    else:
        form = LoanForm(instance=loan)
    return save_loan_form(request, form, 'journal/product_form.html')



def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'journal/index.html', {'loans': loans})


    <script>
        $(document).ready(function(){
            var loadForm = function() {
                var btn = $(this);
                $.ajax({
                    url: btn.attr("data-url"),
                    type: 'get',
                    dataType: 'json',
                    beforeSend: function(){
                        $("#modal-loan .modal-content").html("");
                        $("#modal-loan").modal("show");
                    },
                    success: function(data) {
                        $("#modal-loan .modal-content").html(data.html_form);
                    }
                });
            };

            var saveForm = function() {
                var form = $(this);
                $ajax({
                   url: form.attr("action"),
                   data: form.serialize(),
                   type: form.attr("method"),
                   dataType: 'json',
                   success: function (data) {
                        if (data.form_is_valid) {
                            $("#dataTable tbody").html(data.loan_list);
                            $("#modal-loan").modal("hide");
                        }
                        else {
                            $("#modal-loan .modal-content").html(data.html_form);
                        }
                   }
                });
                return false;
            };

            $(".js-create-loan").click(loadForm);
            $("#modal-loan").on("submit", ".js-loan-create-form", saveForm);
        });

    </script>