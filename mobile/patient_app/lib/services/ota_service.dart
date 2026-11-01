import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:package_info_plus/package_info_plus.dart';
import '../core/config.dart';

class OtaService {
  static Future<void> checkForUpdates() async {
    try {
      final info = await PackageInfo.fromPlatform();
      final build = int.tryParse(info.buildNumber) ?? 100;
      final res = await http.get(Uri.parse(
        '${AppConfig.apiBase}/ota/check/?app=patient&platform=android&build=$build',
      ));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        if (data['update_available'] == true && data['force'] == true) {
          // Show force update dialog in production
        }
      }
    } catch (_) {}
  }
}
