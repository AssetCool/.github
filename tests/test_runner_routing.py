"""Check shared runner selection and preserve issue automation contracts."""

import json
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ("_autocomment-advice.yml", "_autolink-feature-to-epic.yml")


class RunnerRoutingTests(unittest.TestCase):
    def test_shared_workflows_offer_optional_compatible_routing(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                workflow = yaml.safe_load(
                    (ROOT / ".github/workflows" / name).read_text()
                )
                self.assertIsInstance(workflow[True]["workflow_call"], dict)
                inputs = workflow[True]["workflow_call"]["inputs"]
                self.assertFalse(inputs["runner-group"].get("required", False))
                self.assertEqual(inputs["runner-group"]["default"], "")
                self.assertEqual(
                    json.loads(inputs["runner-labels"]["default"]), ["ubuntu-latest"]
                )
                job = next(iter(workflow["jobs"].values()))
                expression = job["runs-on"]
                self.assertIn("inputs.runner-group", expression)
                self.assertIn("toJSON(inputs.runner-group)", expression)
                self.assertIn("fromJSON", expression)
                self.assertIn("inputs.runner-labels ||", expression)
                self.assertEqual(workflow["permissions"], {"issues": "write"})
                self.assertEqual(
                    workflow[True]["issues"]["types"], ["opened", "edited"]
                )
                self.assertEqual(len(job["steps"]), 1)
                self.assertIn("github-script@", job["steps"][0]["uses"])

    def test_routing_expression_for_defaults_opt_in_and_invalid_json(self):
        # Execute the actual workflow expression with the GitHub expression
        # functions used here. actionlint separately validates its GitHub syntax.
        script = r"""
const { expression, inputs } = JSON.parse(process.argv[1]);
const fromJSON = JSON.parse;
const toJSON = JSON.stringify;
function format(template, ...args) {
  return template.replace(/\{(\d+)\}/g, (_, index) => args[index])
    .replaceAll('{{', '{').replaceAll('}}', '}');
}
const code = expression.slice(3, -2)
  .replaceAll('inputs.runner-group', 'inputs["runner-group"]')
  .replaceAll('inputs.runner-labels', 'inputs["runner-labels"]');
console.log(JSON.stringify(eval(code)));
"""
        cases = [
            ({}, ["ubuntu-latest"]),
            (
                {"runner-group": "", "runner-labels": '["ubuntu-latest"]'},
                ["ubuntu-latest"],
            ),
            (
                {
                    "runner-group": "Jetson",
                    "runner-labels": '["self-hosted", "Jetson"]',
                },
                {"group": "Jetson", "labels": ["self-hosted", "Jetson"]},
            ),
            (
                {"runner-labels": '["self-hosted", "Linux", "ARM64"]'},
                ["self-hosted", "Linux", "ARM64"],
            ),
            (
                {"runner-group": 'a"quoted\\group', "runner-labels": '["self-hosted"]'},
                {"group": 'a"quoted\\group', "labels": ["self-hosted"]},
            ),
        ]
        for name in WORKFLOWS:
            job = next(
                iter(
                    yaml.safe_load((ROOT / ".github/workflows" / name).read_text())[
                        "jobs"
                    ].values()
                )
            )
            for inputs, expected in cases:
                with self.subTest(workflow=name, inputs=inputs):
                    result = subprocess.run(
                        [
                            "node",
                            "-e",
                            script,
                            json.dumps(
                                {"expression": job["runs-on"], "inputs": inputs}
                            ),
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.assertEqual(json.loads(result.stdout), expected)
            result = subprocess.run(
                [
                    "node",
                    "-e",
                    script,
                    json.dumps(
                        {
                            "expression": job["runs-on"],
                            "inputs": {"runner-labels": "invalid-json"},
                        }
                    ),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
