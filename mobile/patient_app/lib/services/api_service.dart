import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/config.dart';
import 'secure_storage.dart';

class ApiService {
  static Future<Map<String, String>> _headers() async {
    final token = await SecureStorage.getAccessToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  static Future<http.Response> post(String path, Map<String, dynamic> body) async {
    return http.post(
      Uri.parse('${AppConfig.apiBase}$path'),
      headers: await _headers(),
      body: jsonEncode(body),
    );
  }

  static Future<http.Response> get(String path) async {
    return http.get(Uri.parse('${AppConfig.apiBase}$path'), headers: await _headers());
  }

  static Future<bool> login(String email, String password) async {
    final res = await http.post(
      Uri.parse('${AppConfig.apiBase.replaceAll('/api/v1', '')}/api/v1/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (res.statusCode != 200) return false;
    final data = jsonDecode(res.body);
    await SecureStorage.saveTokens(data['access'], data['refresh']);
    return true;
  }
}
