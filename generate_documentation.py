#!/usr/bin/env python3
"""
Crypto Trading Bot Platform - Documentation Generator

This script generates all documentation artifacts based on the OpenSpec specification
(crypto-trading-bot-platform-docs.openspec.yaml) and the epic data
(JIRA-epic-crypto-trading-bot-platform.md).

Usage:
    python generate_documentation.py [--phase PHASE_NUMBER] [--category CATEGORY_NAME] [--dry-run]
    python generate_documentation.py configure [FLAGS]
    python generate_documentation.py configure          # interactive wizard (no flags)

Examples:
    python generate_documentation.py --phase 1                    # Generate Phase 1 documents only
    python generate_documentation.py --category user_stories      # Generate user stories only
    python generate_documentation.py --dry-run                    # Preview what would be generated
    python generate_documentation.py                              # Generate all documents
    python generate_documentation.py configure -h                 # Show configure help
    python generate_documentation.py configure --list-providers   # List AI providers
    python generate_documentation.py configure --activate-profile anthropic/personal

Author: Development Team
Version: 1.1.0
Date: 2026-03-17
"""

import os
import sys
import yaml
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

# Jinja2 is optional for now (not used in current implementation)
try:
    from jinja2 import Environment, FileSystemLoader, Template
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

# Logger will be configured in main() based on verbosity
logger = logging.getLogger(__name__)


class DocumentGenerator:
    """Main document generator class"""
    
    def __init__(self, openspec_path: str, epic_path: str, output_dir: str, dry_run: bool = False):
        """
        Initialize the document generator.

        Args:
            openspec_path: Path to the OpenSpec YAML file
            epic_path: Path to the epic markdown file
            output_dir: Directory where generated documents will be saved
            dry_run: If True, only preview what would be generated without creating files
        """
        # Resolve paths relative to script directory if not absolute
        script_dir = Path(__file__).parent.resolve()

        self.openspec_path = Path(openspec_path) if Path(openspec_path).is_absolute() else script_dir / openspec_path
        self.epic_path = Path(epic_path) if Path(epic_path).is_absolute() else script_dir / epic_path
        self.output_dir = Path(output_dir) if Path(output_dir).is_absolute() else script_dir / output_dir
        self.dry_run = dry_run
        
        self.spec: Dict[str, Any] = {}
        self.epic_data: Dict[str, Any] = {}
        self.stats = {
            'total': 0,
            'generated': 0,
            'skipped': 0,
            'errors': 0
        }
        
        # Create output directory if it doesn't exist
        if not dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized DocumentGenerator")
        logger.info(f"  OpenSpec: {self.openspec_path}")
        logger.info(f"  Epic: {self.epic_path}")
        logger.info(f"  Output: {self.output_dir}")
        logger.info(f"  Dry Run: {self.dry_run}")
    
    def load_openspec(self) -> None:
        """Load and parse the OpenSpec YAML file"""
        try:
            logger.info(f"Loading OpenSpec from {self.openspec_path}")
            with open(self.openspec_path, 'r', encoding='utf-8') as f:
                self.spec = yaml.safe_load(f)
            logger.info(f"✓ OpenSpec loaded successfully")
        except Exception as e:
            logger.error(f"✗ Failed to load OpenSpec: {e}")
            raise
    
    def load_epic(self) -> None:
        """Load and parse the epic markdown file"""
        try:
            logger.info(f"Loading epic from {self.epic_path}")
            with open(self.epic_path, 'r', encoding='utf-8') as f:
                epic_content = f.read()
            
            self.epic_data = self._parse_epic(epic_content)
            logger.info(f"✓ Epic loaded successfully")
            logger.info(f"  Found {len(self.epic_data.get('stories', []))} stories")
        except Exception as e:
            logger.error(f"✗ Failed to load epic: {e}")
            raise
    
    def _parse_epic(self, content: str) -> Dict[str, Any]:
        """
        Parse the epic markdown file and extract structured data.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Dictionary containing parsed epic data
        """
        epic_data = {
            'metadata': {},
            'stories': [],
            'sprints': [],
            'content': content
        }
        
        # Extract metadata from the epic
        metadata_match = re.search(r'\*\*Epic ID\*\*\s*\|\s*(\S+)', content)
        if metadata_match:
            epic_data['metadata']['epic_id'] = metadata_match.group(1)
        
        # Extract stories (sections starting with "### Story")
        story_pattern = r'### Story \d+: (.+?)\n(.*?)(?=### Story \d+:|## |$)'
        stories = re.finditer(story_pattern, content, re.DOTALL)
        
        for match in stories:
            story_title = match.group(1).strip()
            story_content = match.group(2).strip()
            
            # Extract story ID
            story_id_match = re.search(r'\*\*Story ID\*\*\s*\|\s*(\S+)', story_content)
            story_id = story_id_match.group(1) if story_id_match else None
            
            if story_id:
                epic_data['stories'].append({
                    'id': story_id,
                    'title': story_title,
                    'content': story_content
                })
        
        return epic_data
    
    def generate_all(self, phase: Optional[int] = None, category: Optional[str] = None) -> None:
        """
        Generate all documents or filter by phase/category.
        
        Args:
            phase: Optional phase number to filter (1-10)
            category: Optional category name to filter
        """
        logger.info("=" * 80)
        logger.info("STARTING DOCUMENT GENERATION")
        logger.info("=" * 80)
        
        # Load data
        self.load_openspec()
        self.load_epic()
        
        # Generate documents by category
        if category:
            self._generate_category(category)
        elif phase:
            self._generate_phase(phase)
        else:
            self._generate_all_categories()
        
        # Print summary
        self._print_summary()
    
    def _generate_all_categories(self) -> None:
        """Generate all document categories"""
        categories = [
            'user_stories',
            'technical_design_documents',
            'sprint_planning_documents',
            'development_artifacts',
            'testing_documentation',
            'quality_assurance_documents',
            'deployment_operations_documents',
            'user_facing_documentation',
            'project_management_documents',
            'compliance_governance_documents'
        ]

        for category in categories:
            if category in self.spec:
                self._generate_category(category)

    def _generate_phase(self, phase: int) -> None:
        """Generate documents for a specific phase"""
        logger.info(f"\n{'=' * 80}")
        logger.info(f"GENERATING PHASE {phase} DOCUMENTS")
        logger.info(f"{'=' * 80}")

        workflow = self.spec.get('generation_workflow', {})
        phases = workflow.get('phases', [])

        if not phases:
            logger.warning("No phases defined in OpenSpec workflow")
            return

        if phase < 1 or phase > len(phases):
            logger.error(f"Invalid phase number: {phase}. Must be between 1 and {len(phases)}")
            return

        phase_data = phases[phase - 1]
        phase_name = phase_data.get('name', f'Phase {phase}')
        logger.info(f"Phase {phase}: {phase_name}")

        # Map phases to categories based on the workflow
        phase_category_map = {
            1: ['user_stories'],  # Phase 1: Epic and User Stories
            2: ['technical_design_documents'],  # Phase 2: Technical Design
            3: ['sprint_planning_documents'],  # Phase 3: Sprint Planning
            4: ['development_artifacts'],  # Phase 4: Development
            5: ['testing_documentation'],  # Phase 5: Testing
            6: ['quality_assurance_documents'],  # Phase 6: QA
            7: ['deployment_operations_documents'],  # Phase 7: Deployment
            8: ['user_facing_documentation'],  # Phase 8: User Docs
            9: ['project_management_documents'],  # Phase 9: Project Management
            10: ['compliance_governance_documents']  # Phase 10: Compliance
        }

        categories = phase_category_map.get(phase, [])

        if not categories:
            logger.warning(f"No categories mapped for Phase {phase}")
            return

        logger.info(f"Categories for this phase: {', '.join(categories)}")

        # Generate documents for each category in this phase
        for category in categories:
            if category in self.spec:
                self._generate_category(category)
            else:
                logger.warning(f"Category '{category}' not found in OpenSpec")

    def _generate_category(self, category: str) -> None:
        """Generate all documents in a specific category"""
        logger.info(f"\n{'=' * 80}")
        logger.info(f"GENERATING CATEGORY: {category.upper().replace('_', ' ')}")
        logger.info(f"{'=' * 80}")

        if category not in self.spec:
            logger.warning(f"Category '{category}' not found in OpenSpec")
            return

        category_data = self.spec[category]

        # Handle different category types
        if category == 'user_stories':
            self._generate_user_stories(category_data)
        elif category == 'technical_design_documents':
            self._generate_technical_design_docs(category_data)
        elif category == 'sprint_planning_documents':
            self._generate_sprint_planning_docs(category_data)
        elif category == 'testing_documentation':
            self._generate_testing_docs(category_data)
        else:
            logger.info(f"Generic generation for category: {category}")
            self._generate_generic_category(category, category_data)

    def _generate_user_stories(self, category_data: Dict[str, Any]) -> None:
        """Generate user story documents"""
        story_list = category_data.get('story_list', [])

        logger.info(f"Found {len(story_list)} user stories to generate")

        for story_spec in story_list:
            # Try both 'story_id' and 'id' keys
            story_id = story_spec.get('story_id') or story_spec.get('id')

            if not story_id:
                logger.warning(f"Story spec missing ID: {story_spec}")
                self.stats['skipped'] += 1
                continue

            # Find matching story in epic data
            story_data = self._find_story_in_epic(story_id)

            if not story_data:
                logger.warning(f"Story {story_id} not found in epic data, skipping")
                self.stats['skipped'] += 1
                continue

            # Generate the user story document
            self._generate_user_story_document(story_spec, story_data, category_data)

    def _find_story_in_epic(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Find a story in the parsed epic data"""
        for story in self.epic_data.get('stories', []):
            if story.get('id') == story_id:
                return story
        return None

    def _generate_user_story_document(self, story_spec: Dict[str, Any],
                                     story_data: Dict[str, Any],
                                     category_data: Dict[str, Any]) -> None:
        """Generate a single user story document"""
        story_id = story_spec.get('story_id') or story_spec.get('id')
        story_name = story_spec.get('story_name') or story_spec.get('name', 'untitled')

        # Create title slug from story name
        title_slug = story_name.lower().replace(' ', '-').replace('&', 'and')
        title_slug = re.sub(r'[^a-z0-9-]', '', title_slug)

        filename = f"user-story-{story_id}-{title_slug}.md"
        filepath = self.output_dir / filename

        self.stats['total'] += 1

        # Check if file already exists
        if filepath.exists() and not self.dry_run:
            logger.info(f"  ⊙ {filename} (already exists, skipping)")
            self.stats['skipped'] += 1
            return

        try:
            # Parse story content from epic
            parsed_story = self._parse_story_content(story_data['content'])

            # Generate document content
            content = self._render_user_story_template(
                story_spec,
                parsed_story,
                category_data.get('template_structure', {})
            )

            if self.dry_run:
                logger.info(f"  ✓ {filename} (dry run - would create)")
            else:
                # Write to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"  ✓ {filename} (created)")

            self.stats['generated'] += 1

        except Exception as e:
            logger.error(f"  ✗ {filename} (error: {e})")
            self.stats['errors'] += 1

    def _parse_story_content(self, content: str) -> Dict[str, Any]:
        """Parse story content from epic markdown"""
        parsed = {
            'metadata': {},
            'user_story': '',
            'business_context': '',
            'acceptance_criteria': [],
            'technical_requirements': [],
            'dependencies': [],
            'testing_requirements': '',
            'definition_of_done': []
        }

        # Extract metadata table
        table_pattern = r'\| \*\*(.+?)\*\* \| (.+?) \|'
        for match in re.finditer(table_pattern, content):
            key = match.group(1).strip().lower().replace(' ', '_')
            value = match.group(2).strip()
            parsed['metadata'][key] = value

        # Extract user story
        user_story_match = re.search(
            r'\*\*As a\*\* (.+?)\n\*\*I need\*\* (.+?)\n\*\*So that\*\* (.+?)(?:\n\n|$)',
            content,
            re.DOTALL
        )
        if user_story_match:
            parsed['user_story'] = {
                'role': user_story_match.group(1).strip(),
                'capability': user_story_match.group(2).strip(),
                'benefit': user_story_match.group(3).strip()
            }

        # Extract business context
        business_context_match = re.search(
            r'#### Business Context\n\n(.+?)(?=####|$)',
            content,
            re.DOTALL
        )
        if business_context_match:
            parsed['business_context'] = business_context_match.group(1).strip()

        # Extract acceptance criteria sections
        ac_pattern = r'##### (.+?) \(AC-\d+-\d+\)\n\n(.+?)(?=##### |#### |$)'
        for match in re.finditer(ac_pattern, content, re.DOTALL):
            parsed['acceptance_criteria'].append({
                'title': match.group(1).strip(),
                'content': match.group(2).strip()
            })

        return parsed

    def _render_user_story_template(self, story_spec: Dict[str, Any],
                                    parsed_story: Dict[str, Any],
                                    template_structure: Dict[str, Any]) -> str:
        """Render a user story document from template"""

        metadata = parsed_story.get('metadata', {})
        user_story = parsed_story.get('user_story', {})

        # Build the document
        lines = []

        # Header
        story_id = story_spec.get('story_id') or story_spec.get('id')
        story_name = story_spec.get('story_name') or story_spec.get('name', 'Untitled Story')
        lines.append(f"# User Story: {story_id} - {story_name}")
        lines.append("")
        lines.append("**Document Type**: User Story")
        lines.append("**Document Version**: 1.0.0")
        lines.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"**Document Owner**: {metadata.get('assignee', 'TBD')}")
        lines.append("**Related Epic**: TRADE-001 - Crypto Trading Bot Platform Development")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Metadata table
        lines.append("## Story Metadata")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")

        for key, value in metadata.items():
            display_key = key.replace('_', ' ').title()
            lines.append(f"| **{display_key}** | {value} |")

        lines.append("")
        lines.append("---")
        lines.append("")

        # User Story
        lines.append("## User Story")
        lines.append("")
        if isinstance(user_story, dict):
            lines.append(f"**As a** {user_story.get('role', 'TBD')}")
            lines.append(f"**I need** {user_story.get('capability', 'TBD')}")
            lines.append(f"**So that** {user_story.get('benefit', 'TBD')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Business Context
        lines.append("## Business Context")
        lines.append("")
        lines.append(parsed_story.get('business_context', 'TBD'))
        lines.append("")
        lines.append("---")
        lines.append("")

        # Acceptance Criteria
        lines.append("## Acceptance Criteria")
        lines.append("")
        for i, ac in enumerate(parsed_story.get('acceptance_criteria', []), 1):
            lines.append(f"### AC-{story_id.split('-')[1]}-{i:02d}: {ac.get('title', 'TBD')}")
            lines.append("")
            lines.append(ac.get('content', 'TBD'))
            lines.append("")

        lines.append("---")
        lines.append("")

        # Technical Requirements (placeholder)
        lines.append("## Technical Requirements")
        lines.append("")
        lines.append("*To be extracted from epic data*")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Dependencies (placeholder)
        lines.append("## Dependencies")
        lines.append("")
        lines.append("| Dependency ID | Dependency Name | Relationship Type | Criticality | Notes |")
        lines.append("|--------------|----------------|-------------------|-------------|-------|")
        lines.append("| TBD | TBD | TBD | TBD | TBD |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Testing Requirements (placeholder)
        lines.append("## Testing Requirements")
        lines.append("")
        lines.append("*To be defined*")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Definition of Done
        lines.append("## Definition of Done")
        lines.append("")
        lines.append("- [ ] All acceptance criteria met and verified")
        lines.append("- [ ] Unit test coverage >90%")
        lines.append("- [ ] Code reviewed and approved")
        lines.append("- [ ] Documentation completed")
        lines.append("- [ ] Deployed to staging and verified")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Footer
        lines.append(f"**Document Status**: ⏳ Draft")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        return "\n".join(lines)

    def _generate_technical_design_docs(self, category_data: Dict[str, Any]) -> None:
        """Generate technical design documents"""
        logger.info("Technical design document generation not yet implemented")
        logger.info("  - ADRs: 8 documents")
        logger.info("  - API Specs: 5 documents")
        logger.info("  - DB Schemas: 4 documents")
        logger.info("  - Architecture Diagrams: 3 documents")

    def _generate_sprint_planning_docs(self, category_data: Dict[str, Any]) -> None:
        """Generate sprint planning documents"""
        logger.info("Sprint planning document generation not yet implemented")
        logger.info("  - Sprint Backlogs: 9 documents")
        logger.info("  - Sprint Goals: 9 documents")
        logger.info("  - Capacity Planning: 9 documents")

    def _generate_testing_docs(self, category_data: Dict[str, Any]) -> None:
        """Generate testing documents"""
        logger.info("Testing document generation not yet implemented")
        logger.info("  - Test Plans: Multiple documents")
        logger.info("  - Test Cases: Multiple documents")

    def _generate_generic_category(self, category: str, category_data: Dict[str, Any]) -> None:
        """Generate documents for a generic category"""
        logger.info(f"Generic category generation for '{category}' not yet implemented")

    def _print_summary(self) -> None:
        """Print generation summary"""
        logger.info("")
        logger.info("=" * 80)
        logger.info("GENERATION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total documents:     {self.stats['total']}")
        logger.info(f"  ✓ Generated:       {self.stats['generated']}")
        logger.info(f"  ⊙ Skipped:         {self.stats['skipped']}")
        logger.info(f"  ✗ Errors:          {self.stats['errors']}")
        logger.info("=" * 80)

        if self.dry_run:
            logger.info("DRY RUN MODE - No files were actually created")

        success_rate = (self.stats['generated'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
        logger.info(f"Success rate: {success_rate:.1f}%")


def main():
    """Main entry point"""
    # Get script directory for default paths
    script_dir = Path(__file__).parent.resolve()

    parser = argparse.ArgumentParser(
        description='Generate documentation for Crypto Trading Bot Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate all documents
  %(prog)s --phase 1                          # Generate Phase 1 documents only
  %(prog)s --category user_stories            # Generate user stories only
  %(prog)s --dry-run                          # Preview what would be generated
  %(prog)s --category user_stories --dry-run  # Preview user story generation
  %(prog)s --output ./generated-docs          # Output to specific directory
        """
    )

    parser.add_argument(
        '--phase',
        type=int,
        choices=range(1, 11),
        help='Generate documents for a specific phase (1-10)'
    )

    parser.add_argument(
        '--category',
        type=str,
        choices=[
            'user_stories',
            'technical_design_documents',
            'sprint_planning_documents',
            'development_artifacts',
            'testing_documentation',
            'quality_assurance_documents',
            'deployment_operations_documents',
            'user_facing_documentation',
            'project_management_documents',
            'compliance_governance_documents'
        ],
        help='Generate documents for a specific category'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be generated without creating files'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all output except errors'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available categories and phases, then exit'
    )

    parser.add_argument(
        '--openspec',
        type=str,
        default='crypto-trading-bot-platform-docs.openspec.yaml',
        help='Path to OpenSpec YAML file (default: crypto-trading-bot-platform-docs.openspec.yaml in script directory)'
    )

    parser.add_argument(
        '--epic',
        type=str,
        default='JIRA-epic-crypto-trading-bot-platform.md',
        help='Path to epic markdown file (default: JIRA-epic-crypto-trading-bot-platform.md in script directory)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=str(script_dir),
        help=f'Output directory for generated documents (default: script directory - {script_dir})'
    )

    # ------------------------------------------------------------------
    # Subcommands
    # ------------------------------------------------------------------
    subparsers = parser.add_subparsers(
        dest='subcommand',
        metavar='SUBCOMMAND',
        help='Available subcommands (use SUBCOMMAND -h for details)',
    )

    # configure subcommand — AI provider management
    configure_parser = subparsers.add_parser(
        'configure',
        help='Manage AI provider profiles',
        description=(
            'Configure AI provider profiles for use with AI-powered commands.\n'
            'Run without flags to launch the interactive guided setup wizard.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                         # interactive wizard
  %(prog)s --list-providers                        # list all providers
  %(prog)s --list-profiles                         # list all profiles
  %(prog)s --list-profiles-for-provider anthropic  # list profiles for one provider
  %(prog)s --create-profile anthropic/personal     # create a new profile
  %(prog)s --edit-profile   anthropic/personal     # edit an existing profile
  %(prog)s --delete-profile anthropic/personal     # delete a profile
  %(prog)s --activate-profile anthropic/personal   # set the active profile
        """,
    )

    configure_parser.add_argument(
        '--list-providers',
        action='store_true',
        default=False,
        help='List all registered AI providers',
    )
    configure_parser.add_argument(
        '--list-profiles',
        action='store_true',
        default=False,
        help='List all saved provider profiles',
    )
    configure_parser.add_argument(
        '--list-profiles-for-provider',
        metavar='PROVIDER_ID',
        default=None,
        help='List profiles for a specific provider (e.g. anthropic)',
    )
    configure_parser.add_argument(
        '--create-profile',
        metavar='PROVIDER_ID/PROFILE_NAME',
        default=None,
        help='Create a new profile (e.g. anthropic/personal)',
    )
    configure_parser.add_argument(
        '--edit-profile',
        metavar='PROVIDER_ID/PROFILE_NAME',
        default=None,
        help='Edit an existing profile (e.g. anthropic/personal)',
    )
    configure_parser.add_argument(
        '--delete-profile',
        metavar='PROVIDER_ID/PROFILE_NAME',
        default=None,
        help='Delete a profile (e.g. anthropic/personal)',
    )
    configure_parser.add_argument(
        '--activate-profile',
        metavar='PROVIDER_ID/PROFILE_NAME',
        default=None,
        help='Set the active AI provider/profile (e.g. anthropic/personal)',
    )

    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Dispatch: configure subcommand (early return — bypasses doc gen)
    # ------------------------------------------------------------------
    if args.subcommand == 'configure':
        from ai_providers import ConfigureOptions, configure_command
        options = ConfigureOptions(
            list_providers=args.list_providers,
            list_profiles=args.list_profiles,
            list_profiles_for_provider=args.list_profiles_for_provider,
            create_profile=args.create_profile,
            edit_profile=args.edit_profile,
            delete_profile=args.delete_profile,
            activate_profile=args.activate_profile,
        )
        result = configure_command(options)
        return result if isinstance(result, int) else 0

    # Configure logging based on verbosity
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.ERROR

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('documentation_generation.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Validate arguments
    if args.phase and args.category:
        logger.error("Cannot specify both --phase and --category. Please choose one.")
        return 1

    if args.verbose and args.quiet:
        logger.error("Cannot specify both --verbose and --quiet. Please choose one.")
        return 1

    # Handle --list command
    if args.list:
        print("\n" + "=" * 80)
        print("AVAILABLE CATEGORIES")
        print("=" * 80)
        categories = [
            'user_stories',
            'technical_design_documents',
            'sprint_planning_documents',
            'development_artifacts',
            'testing_documentation',
            'quality_assurance_documents',
            'deployment_operations_documents',
            'user_facing_documentation',
            'project_management_documents',
            'compliance_governance_documents'
        ]
        for i, cat in enumerate(categories, 1):
            print(f"{i:2d}. {cat}")

        print("\n" + "=" * 80)
        print("AVAILABLE PHASES")
        print("=" * 80)
        phases = [
            "Phase 1: Epic and User Stories",
            "Phase 2: Technical Design Documents",
            "Phase 3: Sprint Planning Documents",
            "Phase 4: Development Artifacts",
            "Phase 5: Testing Documentation",
            "Phase 6: Quality Assurance Documents",
            "Phase 7: Deployment & Operations Documents",
            "Phase 8: User-Facing Documentation",
            "Phase 9: Project Management Documents",
            "Phase 10: Compliance & Governance Documents"
        ]
        for i, phase in enumerate(phases, 1):
            print(f"{i:2d}. {phase}")

        print("\n" + "=" * 80)
        print("\nUsage Examples:")
        print("  python generate_documentation.py --category user_stories")
        print("  python generate_documentation.py --phase 1")
        print("  python generate_documentation.py --dry-run")
        print("=" * 80 + "\n")
        return 0

    # Show configuration
    logger.info("=" * 80)
    logger.info("CONFIGURATION")
    logger.info("=" * 80)
    logger.info(f"OpenSpec:     {args.openspec}")
    logger.info(f"Epic:         {args.epic}")
    logger.info(f"Output:       {args.output}")
    logger.info(f"Dry Run:      {args.dry_run}")
    if args.phase:
        logger.info(f"Phase:        {args.phase}")
    if args.category:
        logger.info(f"Category:     {args.category}")
    logger.info("=" * 80)
    logger.info("")

    # Create generator
    try:
        generator = DocumentGenerator(
            openspec_path=args.openspec,
            epic_path=args.epic,
            output_dir=args.output,
            dry_run=args.dry_run
        )
    except Exception as e:
        logger.error(f"Failed to initialize generator: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Generate documents
    try:
        generator.generate_all(phase=args.phase, category=args.category)
        logger.info("\n✓ Document generation completed successfully!")
        return 0
    except Exception as e:
        logger.error(f"\n✗ Document generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

