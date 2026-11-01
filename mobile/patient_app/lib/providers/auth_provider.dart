import 'package:flutter/foundation.dart';
import '../services/api_service.dart';
import '../services/secure_storage.dart';

class AuthProvider extends ChangeNotifier {
  bool isReady = false;
  bool isLoggedIn = false;

  AuthProvider() {
    _init();
  }

  Future<void> _init() async {
    final token = await SecureStorage.getAccessToken();
    isLoggedIn = token != null;
    isReady = true;
    notifyListeners();
  }

  Future<bool> login(String email, String password) async {
    final ok = await ApiService.login(email, password);
    isLoggedIn = ok;
    notifyListeners();
    return ok;
  }

  Future<void> logout() async {
    await SecureStorage.clear();
    isLoggedIn = false;
    notifyListeners();
  }
}
