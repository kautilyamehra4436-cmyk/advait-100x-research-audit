import tempfile, unittest
from pathlib import Path
from b2b_reconcile import analyze_rows, reconcile_text, run, MAX_INPUT_BYTES


class ReconcilePrototypeTests(unittest.TestCase):
    def test_pure_text_api_returns_bounded_report_without_files(self):
        report = reconcile_text(
            "invoice_id,vendor,amount,po_ref,po_amount,po_vendor\n"
            "I1,Acme,10.00,P1,12.00,Acme\n"
        )
        self.assertEqual(report["rows_checked"], 1)
        self.assertEqual(report["flags"], 1)
        self.assertIn("amount_mismatch", report["rule_counts"])
        self.assertIn("I1", report["normalized_csv"])
        self.assertIn("amount_mismatch", report["exceptions_csv"])

    def test_formula_like_text_is_flagged_and_escaped(self):
        report = reconcile_text(
            "invoice_id,vendor,amount,po_ref\n"
            "I1,=HYPERLINK(\"https://bad.example\"),10,P1\n"
        )
        self.assertIn("formula_injection_risk", report["rule_counts"])
        self.assertIn("'=HYPERLINK", report["normalized_csv"])
        self.assertIn("'=HYPERLINK", report["exceptions_csv"])

    def test_duplicate_headers_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate headers"):
            reconcile_text("invoice_id,invoice_id,vendor,amount\nI1,I2,A,10\n")

    def test_malformed_row_width_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "more values"):
            reconcile_text("invoice_id,vendor,amount\nI1,A,10,EXTRA\n")

    def test_oversized_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "1 MiB"):
            reconcile_text("x" * (MAX_INPUT_BYTES + 1))

    def test_duplicate_ids_flag_both_rows(self):
        rows=[{"invoice_id":"I-1","vendor":"A","amount":"10","po_ref":"P1"},{"invoice_id":"i-1","vendor":"A","amount":"10","po_ref":"P2"}]
        self.assertEqual(sum(x["rule"]=="duplicate_invoice_id" for x in analyze_rows(rows)),2)

    def test_missing_po_ref(self):
        f=analyze_rows([{"invoice_id":"I1","vendor":"A","amount":"10","po_ref":""}])
        self.assertIn("missing_po_reference",[x["rule"] for x in f])

    def test_amount_mismatch(self):
        f=analyze_rows([{"invoice_id":"I1","vendor":"A","amount":"10.00","po_ref":"P1","po_amount":"12.00"}])
        self.assertEqual(sum(x["rule"]=="amount_mismatch" for x in f),1)

    def test_vendor_mismatch_case_insensitive_trim(self):
        f=analyze_rows([{"invoice_id":"I1","vendor":" Acme ","amount":"10","po_ref":"P1","po_vendor":"acme"}])
        self.assertNotIn("vendor_mismatch",[x["rule"] for x in f])

    def test_vendor_mismatch_flag(self):
        f=analyze_rows([{"invoice_id":"I1","vendor":"Acme Ltd","amount":"10","po_ref":"P1","po_vendor":"ACME"}])
        self.assertIn("vendor_mismatch",[x["rule"] for x in f])

    def test_invalid_amount(self):
        f=analyze_rows([{"invoice_id":"I1","vendor":"A","amount":"ten","po_ref":"P1"}])
        self.assertIn("invalid_amount",[x["rule"] for x in f])

    def test_missing_fields(self):
        f=analyze_rows([{"invoice_id":"","vendor":"","amount":"","po_ref":""}])
        rules={x["rule"] for x in f}
        self.assertTrue({"missing_invoice_id","missing_vendor","missing_amount"} <= rules)

    def test_input_not_overwritten_and_outputs_created(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"input.csv"
            source.write_text("invoice_id,vendor,amount,po_ref\nI1,A,10,P1\n",encoding="utf-8")
            before=source.read_bytes()
            _,outputs=run(source,Path(d)/"out")
            self.assertEqual(source.read_bytes(),before)
            with self.assertRaises(FileExistsError):
                run(source,Path(d)/"out")
            self.assertTrue(all(p.exists() for p in outputs))
            self.assertIn("Rows checked: 1",(Path(d)/"out_summary.txt").read_text())

    def test_required_columns_error(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"bad.csv"
            source.write_text("invoice_id,amount\nI1,10\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                run(source,Path(d)/"out")


if __name__=="__main__":
    unittest.main()
