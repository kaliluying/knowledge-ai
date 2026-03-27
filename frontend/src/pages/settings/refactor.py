import re

with open('/Users/gemaolin/code/knowledge-ai/frontend/src/pages/settings/Settings.vue', 'r') as f:
    content = f.read()

# Split into script, template, style
script_match = re.search(r'<script.*?</script>', content, re.DOTALL)
style_match = re.search(r'<style scoped>(.*?)</style>', content, re.DOTALL)

if not style_match:
    print("Could not find style scoped")
    exit(1)

style_content = style_match.group(1)

# Modify CSS to use :deep() for all classes except .settings-page, .page-header, .settings-layout, .settings-sidebar, .tab-btn, .logout-section, .logout-btn, .settings-content
# Actually, an easier way is to just wrap the whole thing down with `:deep()`? No.
# Just extract styles to settings-shared.css and import it in every child component?
# Yes! If we create settings-shared.css and use `@import '../settings-shared.css';` in every child component's <style scoped>!

with open('/Users/gemaolin/code/knowledge-ai/frontend/src/pages/settings/settings-shared.css', 'w') as f:
    f.write(style_content)

print("Created settings-shared.css")
