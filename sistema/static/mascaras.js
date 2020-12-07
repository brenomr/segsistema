$(document).ready(function(){
  $('#id_cpf').mask('000.000.000-00');
  $('#id_telefone').mask('(19) 0000-0000');
  $('#id_celular').mask('(00) 00000-0000');
  $('#id_placa').mask('AAA 0000');
  $('.time').mask('00:00:00');
  $('.date_time').mask('00/00/0000 00:00:00');
  $('.cep').mask('00000-000');
  $('.phone_with_ddd').mask('(00) 0000-0000');

  $('.mixed').mask('AAA 000-S0S');
  $('.ip_address').mask('099.099.099.099');
  $('.percent').mask('##0,00%', {reverse: true});
  $('.clear-if-not-match').mask("00/00/0000", {clearIfNotMatch: true});
  $('.placeholder').mask("00/00/0000", {placeholder: "__/__/____"});
  })