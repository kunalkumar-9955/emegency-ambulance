import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';

class VoiceAssistant {
  final _stt = SpeechToText();
  final _tts = FlutterTts();
  String _locale = 'en_IN';

  final _commands = {
    'book ambulance': 'sos',
    'ambulance book karo': 'sos',
    'call nearest hospital': 'hospital',
    'share my location': 'location',
    'mera location share karo': 'location',
  };

  Future<String?> listen() async {
    if (!await _stt.initialize()) return null;
    String? result;
    await _stt.listen(
      localeId: _locale,
      onResult: (r) => result = r.recognizedWords.toLowerCase(),
    );
    await Future.delayed(const Duration(seconds: 4));
    await _stt.stop();
    if (result == null) return null;
    for (final entry in _commands.entries) {
      if (result!.contains(entry.key)) return entry.value;
    }
    return null;
  }

  Future<void> speak(String text, {String lang = 'en'}) async {
    await _tts.setLanguage(lang == 'hi' ? 'hi-IN' : 'en-US');
    await _tts.speak(text);
  }

  void setLanguage(String code) => _locale = code == 'hi' ? 'hi_IN' : 'en_IN';
}
