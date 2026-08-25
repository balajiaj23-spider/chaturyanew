from django.core.management.base import BaseCommand
from workshop.models import SiteSettings, PreviousEvent, Course, CourseTopic, CourseProject

class Command(BaseCommand):
    help = 'Seeds initial database content for Chathurya Student Developers Club Workshop Website'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Site Settings
        settings = SiteSettings.load()
        settings.club_name = 'Chathurya Student Developers Club'
        settings.college_name = 'Tech Campus, College Block B'
        settings.hero_title = 'Learn. Build. Launch.'
        settings.hero_subtitle = 'Welcome to Chathurya Student Developers Club. Join our hands-on technical workshops designed to help students build practical skills, explore modern software technologies, and launch real-world projects.'
        settings.about_text = 'Chathurya Student Developers Club is a premier student-led technical community dedicated to nurturing coding talent, practical software engineering, and data science skills.'
        settings.contact_email = 'chathurya.club@college.edu'
        settings.contact_phone = '+91 98765 43210'
        settings.address = 'Tech Building Block B, Innovation Way, College Campus, 560100'
        settings.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site Settings initialized."))

        # 2. Previous Events
        PreviousEvent.objects.all().delete()
        
        event1 = PreviousEvent.objects.create(
            title='CS50P – Introduction to Programming with Python',
            description='CS50P, or CS50’s Introduction to Programming with Python, is a free online course by Harvard University taught by David J. Malan. It focuses entirely on learning how to write code, test, and debug using the Python programming language. It is open to complete beginners and requires no prior coding experience.',
            image_path='images/cs50p.svg',
            date_str='2025 – 2026',
            year='2026',
            display_order=1,
            is_active=True
        )

        event2 = PreviousEvent.objects.create(
            title='WebStart 2.0',
            description='A Web Start workshop is a beginner-friendly crash course or training program for students. It teaches the core blocks of web development from scratch. Students learn how to build and design their very first interactive websites.',
            image_path='images/webstart.svg',
            date_str='2025',
            year='2025',
            display_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS("[OK] Previous Events seeded (CS50P & WebStart 2.0)."))

        # 3. Courses
        Course.objects.all().delete()

        # Course 1: Full Stack Development
        c1 = Course.objects.create(
            title='Full Stack Development',
            slug='fullstack',
            badge_text='5-Day Workshop',
            short_description='Master end-to-end web application development. Learn HTML, CSS, SQL, Python, Flask, and Git version control.',
            detailed_description='Learn how modern websites and web applications are built from scratch. Master frontend UI layout, backend APIs, SQLite database design, and Flask web deployment with Chathurya Student Developers Club.',
            image_path='images/fullstack.svg',
            duration='5 Days (Intensive Sessions)',
            who_can_attend='Students from any stream interested in web development.',
            requirements='Basic computer knowledge, Laptop recommended, Enthusiasm to code and build',
            capstone_title='College Canteen Pre-Order System',
            capstone_description='Build and test a College Canteen Pre-Order System from start to finish using all the technologies learned during the workshop.',
            capstone_tech_flow='Frontend (HTML & CSS) -> Database (SQLite) -> Backend Logic (Python) -> Web App (Flask) -> Test, Run & Deliver',
            display_order=1,
            is_active=True
        )

        # Topics for Full Stack
        fs_topics = [
            ('01', 'HTML', 'Structure real web pages\nForms and input elements\nTables and data display\nSemantic tags', 1),
            ('02', 'CSS', 'Responsive layouts\nFlexbox for alignment\nGrid for complex layouts\nStyling and themes\nReusable components', 2),
            ('03', 'SQL / SQLite', 'Tables and columns\nRelationships\nCRUD queries\nDatabase design', 3),
            ('04', 'PYTHON', 'Variables and data types\nData structures (list, dict, etc.)\nFunctions and modules\nError handling\nObject-oriented basics', 4),
            ('05', 'FLASK', 'Routes and URL handling\nTemplates and rendering\nForms and validation\nSessions and user state\nCRUD web apps', 5),
            ('06', 'GIT & VS CODE', 'Version control with Git\nBranching and merging\nCommits and history\nDebugging and workflow\nProject workflow', 6),
        ]
        for mod, title, bullets, order in fs_topics:
            CourseTopic.objects.create(course=c1, module_number=mod, section_title=title, bullets=bullets, display_order=order)

        # Projects for Full Stack
        fs_projects = [
            'Build a Responsive Canteen Menu',
            'Design an Order Database',
            'Create a Python Order Calculator',
            'Develop a Flask Pre-Order Web App',
            'Integrate the Complete Full-Stack Project'
        ]
        for i, p_title in enumerate(fs_projects, 1):
            CourseProject.objects.create(course=c1, title=p_title, display_order=i)

        # Course 2: Data Analytics
        c2 = Course.objects.create(
            title='Data Analytics',
            slug='data-analytics',
            badge_text='5-Day Workshop',
            short_description='Master data cleaning, advanced Excel formulas, Power Pivot data modeling, VBA automation, and Tableau analytics dashboards.',
            detailed_description='Master Excel data cleaning, Power Query, advanced formulas, Power Pivot data modeling, VBA automation, and Tableau analytics dashboards with Chathurya Student Developers Club.',
            image_path='images/data-analytics.svg',
            duration='5 Days (Intensive Lab)',
            who_can_attend='Students interested in data, analytics, Excel, or Tableau.',
            requirements='Basic computer knowledge, Laptop recommended, No prior coding experience required',
            capstone_title='Sales and Operations Analytics Dashboard',
            capstone_description='Build and test a complete Sales and Operations Analytics Dashboard from raw data to actionable insights using Excel, Power Query, Power Pivot, VBA, and Tableau.',
            capstone_tech_flow='Excel -> Power Query -> Power Pivot -> VBA -> Tableau',
            display_order=2,
            is_active=True
        )

        # Topics for Data Analytics
        da_topics = [
            ('01', 'EXCEL DATA CLEANING', 'Import CSV and web data\nClean messy values\nMerge files\nPower Query', 1),
            ('02', 'ADVANCED EXCEL', 'XLOOKUP\nINDEX-MATCH\nDynamic ranges\nConditional logic\nText and date functions', 2),
            ('03', 'DATA MODELING', 'Power Pivot\nRelationships\nCalculated columns\nMeasures\nFinancial modeling basics', 3),
            ('04', 'AUTOMATION', 'Pivot tables\nSlicers\nVBA macros\nLoops\nUser-defined functions', 4),
            ('05', 'TABLEAU ANALYTICS', 'Connect Excel/CSV\nJoins\nDimensions and measures\nChart types\nCalculated fields', 5),
            ('06', 'DASHBOARDS & STORYTELLING', 'Filters\nParameters\nMaps\nClustering\nDashboard design\nPublishing and presenting insights', 6),
        ]
        for mod, title, bullets, order in da_topics:
            CourseTopic.objects.create(course=c2, module_number=mod, section_title=title, bullets=bullets, display_order=order)

        # Projects for Data Analytics
        da_projects = [
            'Clean a 50,000-row dataset',
            'Build a relational Excel model',
            'Automate repetitive tasks with VBA',
            'Create interactive Tableau charts',
            'Develop a three-page executive dashboard'
        ]
        for i, p_title in enumerate(da_projects, 1):
            CourseProject.objects.create(course=c2, title=p_title, display_order=i)

        self.stdout.write(self.style.SUCCESS("[OK] Courses, Modules, Projects, and Capstones seeded."))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] Seeding complete! Database is ready."))
