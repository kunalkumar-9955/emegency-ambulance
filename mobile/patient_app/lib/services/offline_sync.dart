import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'api_service.dart';

class OfflineSync {
  static Database? _db;

  static Future<Database> get database async {
    if (_db != null) return _db!;
    final path = join(await getDatabasesPath(), 'emergency_offline.db');
    _db = await openDatabase(path, version: 1, onCreate: (db, _) async {
      await db.execute('''
        CREATE TABLE pending_sos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          payload TEXT NOT NULL,
          sync_id TEXT UNIQUE,
          created_at TEXT
        )
      ''');
    });
    return _db!;
  }

  static Future<void> queueSOS(Map<String, dynamic> payload, String syncId) async {
    final db = await database;
    await db.insert('pending_sos', {
      'payload': payload.toString(),
      'sync_id': syncId,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  static Future<void> syncAll() async {
    final db = await database;
    final rows = await db.query('pending_sos');
    for (final row in rows) {
      // Parse and sync when online
      await ApiService.post('/emergencies/sos/', {});
      await db.delete('pending_sos', where: 'id = ?', whereArgs: [row['id']]);
    }
  }
}
