import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/emergency_provider.dart';
import '../services/map_integration.dart';
import '../services/voice_assistant.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final emergency = context.watch<EmergencyProvider>();
    final voice = VoiceAssistant();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Emergency'),
        actions: [
          IconButton(
            icon: const Icon(Icons.map_outlined),
            tooltip: 'Open map',
            onPressed: () => PatientMapIntegration.openMapScreen(context),
          ),
          IconButton(
            icon: const Icon(Icons.mic),
            onPressed: () async {
              final cmd = await voice.listen();
              if (cmd == 'sos' && context.mounted) {
                await context.read<EmergencyProvider>().triggerSOS();
              }
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (emergency.activeEmergencyId != null) ...[
              const Text('Ambulance dispatched', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Text('ETA: ${emergency.etaMinutes ?? '—'} min'),
              const SizedBox(height: 12),
              FilledButton.icon(
                onPressed: () {
                  if (emergency.patientLocation == null) return;
                  PatientMapIntegration.openLiveTracking(
                    context,
                    emergencyId: emergency.activeEmergencyId!,
                    patient: emergency.patientLocation!,
                    destination: emergency.destinationLocation,
                  );
                },
                icon: const Icon(Icons.map),
                label: const Text('Live Tracking Map'),
              ),
              const SizedBox(height: 24),
            ],
            GestureDetector(
              onTap: emergency.isLoading ? null : () => emergency.triggerSOS(),
              child: Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: emergency.isLoading ? Colors.grey : const Color(0xFFDC2626),
                  boxShadow: [BoxShadow(color: Colors.red.withValues(alpha: 0.4), blurRadius: 24, spreadRadius: 4)],
                ),
                child: Center(
                  child: emergency.isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('SOS', style: TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Tap for emergency ambulance', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 48),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _NavChip(icon: Icons.person, label: 'Profile', onTap: () {}),
                _NavChip(icon: Icons.history, label: 'History', onTap: () {}),
                _NavChip(
                  icon: Icons.map,
                  label: 'Map',
                  onTap: () => PatientMapIntegration.openMapScreen(context),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _NavChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  const _NavChip({required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Column(
        children: [
          Icon(icon, size: 28),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}
