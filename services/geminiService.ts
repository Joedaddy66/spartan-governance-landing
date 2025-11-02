
import { GoogleGenAI, Type } from "@google/genai";
import { PromoPack } from '../types';

// The API key is expected to be set in the environment variables.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY! });

const promoPackSchema = {
  type: Type.OBJECT,
  properties: {
    videoScripts: {
      type: Type.OBJECT,
      properties: {
        fifteenSecond: {
          type: Type.STRING,
          description: "A punchy, 15-second video script for platforms like TikTok or Reels. Should be concise and engaging."
        },
        thirtySecond: {
          type: Type.STRING,
          description: "A slightly more detailed 30-second video script. It can include 2-3 quick tips."
        }
      },
      required: ["fifteenSecond", "thirtySecond"]
    },
    thumbnailIdeas: {
      type: Type.ARRAY,
      items: {
        type: Type.STRING,
        description: "A compelling, click-worthy title for a YouTube thumbnail. Use ALL CAPS. e.g., '0 TO 5 CLIENTS (FAST)'"
      },
      description: "A list of 3-4 short, high-impact text ideas for video thumbnails."
    },
    socialMediaCaption: {
      type: Type.STRING,
      description: "A ready-to-post social media caption for platforms like Twitter, LinkedIn, or Instagram. Should include relevant hashtags."
    }
  },
  required: ["videoScripts", "thumbnailIdeas", "socialMediaCaption"]
};


export async function generatePromoPack(topic: string, useThinkingMode: boolean = false): Promise<PromoPack> {
  try {
    const prompt = `You are a world-class marketing expert specializing in content for side hustlers and entrepreneurs. Your task is to generate a complete promotional package for a given topic.

Topic: "${topic}"

Generate the following assets based on this topic. Ensure the tone is helpful, direct, and action-oriented.`;
    
    const model = useThinkingMode ? 'gemini-2.5-pro' : 'gemini-2.5-flash';
    const config: any = {
        responseMimeType: "application/json",
        responseSchema: promoPackSchema,
    };

    if (useThinkingMode) {
        config.thinkingConfig = { thinkingBudget: 32768 };
    }


    const response = await ai.models.generateContent({
      model: model,
      contents: prompt,
      config: config,
    });

    const jsonText = response.text.trim();
    const parsedData = JSON.parse(jsonText);

    // Basic validation
    if (
      !parsedData.videoScripts ||
      !parsedData.thumbnailIdeas ||
      !parsedData.socialMediaCaption
    ) {
      throw new Error("Invalid data structure received from API.");
    }
    
    return parsedData as PromoPack;

  } catch (error) {
    console.error("Error generating promo pack:", error);
    throw new Error("Failed to generate content from the AI. This could be due to an issue with the API key or a network problem.");
  }
}