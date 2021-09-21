 jQuery.noConflict();
        jQuery(function($){
            /*script das mascaras e selects */
            $('select').select2();
            $("#id_telefone").mask("(099) 9999-9999");
            $("#id_hora").mask("99:99");


        /*script que marca os pontos no calendario*/
           var eventDates = [1, 10, 12, 22],
           /*dias fixados*/
            $picker = $('.datepicker-here'),
            $content = $('#custom-cells-events'),
            sentences = [
                'Lorem ipsum dolor sit amet, consectetur ,  ',
                'Ratio quidem vestra sic cogit. Illi enim . ',
                'Duo Reges: constructio interrete. A mene tu?  ',
                'Poterat autem inpune; Qui est in parvis malis.'
            ]
        $picker.datepicker({
            language: 'pt',
            onRenderCell: function (date, cellType) {
                var currentDate = date.getDate();
                if (cellType == 'day' && eventDates.indexOf(currentDate) != -1) {
                    return {
                        html: currentDate + '<span class="dp-note"></span>'
                    }
                }
            },
            onSelect: function onSelect(fd, date) {
                var title = '', content = ''
                if (date && eventDates.indexOf(date.getDate()) != -1) {
                    title = fd;
                    content = sentences[Math.floor(Math.random() * eventDates.length)];
                }
                $('strong', $content).html(title)
                $('p', $content).html(content)
            }
        })
        var currentDate = new Date();
        $picker.data('datepicker').selectDate(new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate())) 
            });