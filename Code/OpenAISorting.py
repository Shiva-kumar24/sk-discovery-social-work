import openai
import pandas as pd
import os


os.environ["OPENAI_API_KEY"] = "API-Key"
openai.api_key = os.environ["OPENAI_API_KEY"]

nasw_comment = """Dear Administrator Brooks-LaSure:
On behalf of the National Association of Social Workers (NASW), I am submitting comments on the notice of proposed rulemaking (NPRM) on CMS–3442–P (RIN 0938–AV25), which addresses nurse minimum staffing standards for long-term care (LTC) facilities and Medicaid institutional payment transparency reporting.
Founded in 1955, NASW is the largest membership organization of professional social workers in the United States, representing more than 110,000 social workers. We work to enhance the professional growth and development of our members, to create and maintain professional standards, and to advance sound social policies.
Social workers are integral members of interdisciplinary teams within LTC facilities (hereafter also referred to as “nursing homes”). These teams include three nursing disciplines: certified nursing assistants (CNAs), licensed practical nurses–licensed vocational nurses (LPNs–LVNs), and registered nurses (RNs). Social workers and nursing staff strive to enhance the quality of life and quality of care for residents. Yet, their efforts are often hindered by exceedingly high workloads.
NASW has long supported the Nursing Home Reform Act of 1986 (S. 2604), which was signed into law as part of the Omnibus Budget Reconciliation Act of 1987 (P.L. 100-203, hereafter “OBRA ‘87”). This law requires the Secretary of Health and Human Services (HHS) to assure that facilities provide each resident with high-quality care and grants the Secretary full authority to set minimum staffing standards. OBRA ’87 also requires facilities to spend Medicare and Medicaid payments on resident care without diverting those public funds to profits, management fees, or inflated payments to self-related parties.
Consequently, NASW has strongly supported the Biden Administration’s initiative to improve the quality of care in nursing homes, of which the current NPRM is a primary component. The NPRM represents a paradigm shift in nursing home oversight to promote quality of care. For decades, health researchers, geriatricians, nurses, and other experts have recommended minimum nursing staffing requirements to improve the quality of care at nursing homes; a wide range of peer-reviewed literature demonstrates the connection between nursing home staffing and quality of care.
As early as 2001, a study by Abt Associates Inc., conducted for the Centers for Medicare & Medicaid Services (CMS), noted the “strong and compelling” evidence for minimum staffing levels, even in an economy with a chronic workforce shortage. Moreover, a blue-ribbon panel convened by the National Academies of Sciences, Engineering, and Medicine (NASEM) noted in its 2022 report that increasing overall nurse staffing (including RN staffing 24 hours per day, seven days per week) has been a consistent and long-standing recommendation for improving the quality of care in nursing homes. Likewise, the NASEM report addressed the importance of professional qualifications for nursing home social workers and made clear the impact of financial transparency and accountability on quality of care."""

comments_df = pd.read_csv('/Users/shiva/Desktop/bin1_classified.csv')
print(comments_df.columns)  

for index, row in comments_df.iterrows():
    comment = row['bin1_cleaned']
    response = openai.chat.completions.create(
                    model="gpt-4o", 
                    messages=[
                        {"role": "system", "content": "You are an expert social worker that is passionate about your job and need to compare the National Association of Social Workers comment to public comments about a proposed rule on minimum staffing at nursing homes. "},

                        {"role": "user", "content": f"Does the public comment have similar template language but is different from the NASW comment? If yes provide a 3 word summary on what is different, if not don't say anything.  \n\nNASW comment:\n{nasw_comment}\n\nPublic comment:\n{comment}"}
                    ]
                )
    break

comparison_results = []

for index, row in comments_df.iterrows():
    comment = row['bin1_cleaned']
    response = openai.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": "You are an expert social worker that is passionate about your job and need to compare the National Association of Social Workers comment to public comments about a proposed rule on minimum staffing at nursing homes. "},

                    {"role": "user", "content": f"Does the public comment have similar template language but is different from the NASW comment? If yes provide a 3 word summary on what is different, if not don't say anything.  \n\nNASW comment:\n{nasw_comment}\n\nPublic comment:\n{comment}"}
                ]
            )
        
        # Extract the result from the response
    result = response.choices[0].message.content
    comparison_results.append(result)
        

comments_df['Comparison_Result'] = comparison_results
comments_df.to_csv('/Users/shiva/Desktop/updated_bin1_comments_3words.csv', index=False)