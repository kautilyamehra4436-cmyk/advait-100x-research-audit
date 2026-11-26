# Advait CEO Control Board v0.1

A read-only control board that brings separate project reports and runtime workstreams into one status view.

## Generate a board

From a checkout of this repository:

```sh
python ceo_control_board.py --root . --root ../my-brain --root ../advait_os --root ../advait_pure_sharp
```

The command writes:
- `reports/ceo-board/CEO_CONTROL_BOARD.md`
- `reports/ceo-board/ceo_control_board.json`

The board searches for known artifacts in the supplied checkout roots. It reports missing evidence as pending and never infers production status from a report filename.

## What this is / is not

- It is a local, read-only reporting board.
- It is not a hosted dashboard, always-on agent, task executor, or real-time telemetry service.
- It does not contact customers, submit bids, publish content, or move money.
- Phone deployment and 24-hour target-device soak remain separate gates.
- A documented component or code foundation is not proof of deployed operation.

## Tests

```sh
python -m unittest tests.test_ceo_control_board -v
```
