def generate_report(source_db: str, target_db: str, validation_result):
	"""Generate a simple migration report summary.

	Returns a dictionary containing a short summary and the
	validation result (converted to dict if possible).
	"""
	report = {
		"summary": f"Migration from {source_db} to {target_db}",
		"valid": True,
	}

	try:
		# If validation_result has to_dict(), use it.
		report["validation"] = (
			validation_result.to_dict()
			if hasattr(validation_result, "to_dict")
			else validation_result
		)
		if hasattr(report["validation"], "get") and report["validation"].get("valid") is False:
			report["valid"] = False
	except Exception:
		report["validation"] = str(validation_result)

	return report


if __name__ == "__main__":
	# Quick smoke test
	class Dummy:
		def to_dict(self):
			return {"valid": True, "errors": [], "warnings": []}

	print(generate_report("mysql", "postgresql", Dummy()))

