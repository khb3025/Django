function onoff_click() {

    if ($('.logo_symbol_gnb').css('display') == 'block') {
        $('.logo_symbol_gnb').css('display', 'none');
    } else {
        $('.logo_symbol_gnb').css('display', 'block');
    }

    if ($('.ico_hide1').css('display') == 'block') {
        $('.ico_hide1').css('display', 'none'); 	
    } else {
        $('.ico_hide1').css('display', 'block');
    }


    if ($('.ico_hide2').css('display') == 'block') {
        $('.ico_hide2').css('display', 'none'); 	
    } else {
        $('.ico_hide2').css('display', 'block');
    }

    if ($('.small_tag').css('padding') == '30px 25px') {
        $('.small_tag').css('padding', '12px 35px');
        $('.small_tag').css('text-align', 'left');
        $('.nav-active-menu').css('top', '0');
        $('.ico_menu').css('display', 'inline-block');
        $('.nav-children').css('display', 'block');
        $('.small_text').css('margin-left', '10px');
        $('.nano-pt20').css('padding-top', '20px');
        $('.active-text').css('color', '#263238');
        $('.logo_gnb').css('display', 'block');
    } else {
        $('.small_tag').css('padding', '30px 25px');
        $('.small_tag').css('text-align', 'center');
        $('.nav-active-menu').css('top', '20px');
        $('.ico_menu').css('display', 'none');
        $('.nav-children').css('display', 'none');
        $('.small_text').css('margin-left', '0');
        $('.nano-pt20').css('padding-top', '0');
        $('.active-text').css('color', '#ff6f00');
        $('.logo_gnb').css('display', 'none');
    }
}



  $('input[type="file"]').on('change', function(e){
    var fileName = e.target.files[0].name;
    if (fileName) {
      $(e.target).parent().attr('data-message', fileName);
    }
  });
  
  $(document).on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    if ($('input[type="file"]').length) {
      if (['dragover', 'dragenter'].indexOf(e.type) > -1) {
        if (window.dragTimeout)
          clearTimeout(window.dragTimeout);
        $('body').addClass('dragged');
      } else if (['dragleave', 'drop'].indexOf(e.type) > -1) {
        // Without the timeout, some dragleave events are triggered
        // when the :after appears, making it blink...
        window.dragTimeout = setTimeout(function() {
          $('body').removeClass('dragged');
        }, 100);
      }
    }
  });