/*
СR�Ƽ� XiaoRGEEK ����ģʽ���ƻ�������������
��ע�⣺���������л����񹲺͹�����Ȩ����������δ������������ҵĿ�ģ�СR�Ƽ���������С�����ͿƼ����޹�˾����������Ȩ���ϣ�
����Home:www.xiao-r.com
*/

var bleno = require('../..');
var XiaoRService = require('./xiaor-service');

var primaryService = new XiaoRService();

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising('XiaoRGEEK', [primaryService.uuid]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
    bleno.setServices([primaryService], function(error){
      console.log('setServices: '  + (error ? 'error ' + error : 'success'));
    });
  }
});
